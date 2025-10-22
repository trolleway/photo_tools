#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
from typing import List, Tuple
from PyQt6 import QtWidgets, QtCore

# Ensure exiftool.exe is in same folder as script
SCRIPT_DIR = Path(__file__).resolve().parent
EXIFTOOL = SCRIPT_DIR / "exiftool.exe"
assert EXIFTOOL.exists(), f"exiftool.exe not found in {SCRIPT_DIR}"

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".mts", ".m2ts", ".3gp", ".flv"}


def list_video_files(folder: Path) -> List[Path]:
    files = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS:
            files.append(p)
    return files


def write_xmp_sidecar(video_path: Path, lat: str, lon: str) -> subprocess.CompletedProcess:
    sidecar_path = video_path.with_suffix(".xmp")
    cmd = [
        str(EXIFTOOL),
        f"-XMP:GPSLatitude={lat}",
        f"-XMP:GPSLongitude={lon}",
        "-overwrite_original",
        "-o",
        str(sidecar_path),
        str(video_path),
    ]
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def parse_coordinates(text: str) -> Tuple[str, str]:
    """
    Accepts strings like:
      "55.547632, 38.186301"
      "55.547632,38.186301"
      " 55.547632 , 38.186301 "
    Returns (lat, lon) as stripped strings or raises ValueError.
    """
    if not text:
        raise ValueError("Empty coordinates")
    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError("Coordinates must contain exactly one comma separating lat and lon")
    lat_s = parts[0].strip()
    lon_s = parts[1].strip()
    # Basic numeric validation
    try:
        _ = float(lat_s)
        _ = float(lon_s)
    except ValueError:
        raise ValueError("Latitude and longitude must be decimal numbers")
    return lat_s, lon_s


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video GPS sidecar setter")
        self.resize(800, 480)

        # Widgets
        self.folder_btn = QtWidgets.QPushButton("Open folder")
        self.folder_label = QtWidgets.QLabel("No folder selected")
        self.file_list = QtWidgets.QListWidget()
        self.coords_input = QtWidgets.QLineEdit()
        self.coords_input.setPlaceholderText("Paste coordinates like: 55.547632, 38.186301")
        self.set_btn = QtWidgets.QPushButton("Set GPS and write .xmp sidecar")
        self.status = QtWidgets.QLabel("")

        # Layout
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.folder_btn)
        left_layout.addWidget(self.folder_label)
        left_layout.addWidget(self.file_list)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Coordinates (lat, lon)", self.coords_input)
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addLayout(form_layout)
        right_layout.addWidget(self.set_btn)
        right_layout.addStretch()
        right_layout.addWidget(self.status)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)

        # Signals
        self.folder_btn.clicked.connect(self.on_open_folder)
        self.set_btn.clicked.connect(self.on_set_gps)
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.current_folder: Path | None = None

    def on_open_folder(self):
        dlg = QtWidgets.QFileDialog(self, "Select folder with video files")
        dlg.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if dlg.exec():
            folder = Path(dlg.selectedFiles()[0])
            self.current_folder = folder
            self.folder_label.setText(str(folder))
            self.populate_file_list(folder)

    def populate_file_list(self, folder: Path):
        self.file_list.clear()
        files = list_video_files(folder)
        for p in files:
            item = QtWidgets.QListWidgetItem(p.name)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, str(p))
            self.file_list.addItem(item)
        self.status.setText(f"{len(files)} video(s) found")

    def selected_video_path(self) -> Path | None:
        item = self.file_list.currentItem()
        if item:
            return Path(item.data(QtCore.Qt.ItemDataRole.UserRole))
        return None

    def on_item_double_clicked(self, item: QtWidgets.QListWidgetItem):
        path = Path(item.data(QtCore.Qt.ItemDataRole.UserRole))
        self.status.setText(f"Selected: {path.name}")

    def on_set_gps(self):
        path = self.selected_video_path()
        if not path:
            self.status.setText("No video selected")
            return

        coords_text = self.coords_input.text().strip()
        try:
            lat, lon = parse_coordinates(coords_text)
        except ValueError as e:
            self.status.setText(str(e))
            return

        self.status.setText("Writing sidecar with exiftool...")
        QtWidgets.QApplication.processEvents()

        proc = write_xmp_sidecar(path, lat, lon)
        if proc.returncode == 0:
            sidecar = path.with_suffix(".xmp")
            self.status.setText(f"Sidecar written: {sidecar.name}")
        else:
            err = proc.stderr.strip() or proc.stdout.strip()
            self.status.setText(f"exiftool failed: {err}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
