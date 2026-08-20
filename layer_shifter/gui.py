# layer_shifter/gui.py
import warnings
from argparse import Namespace
from pathlib import Path

import PySimpleGUI as sg

from layer_shifter.main import run


def run_gui():

    # Путь к папке, где находится gui.py
    GUI_DIR = Path(__file__).parent

    # Путь к иконке (если она в подпапке graph/)
    ICON_PATH = GUI_DIR / "graph" / "icon.ico"

    warnings.filterwarnings("ignore")
    """Запускает графический интерфейс и вызывает основную логику."""
    sg.theme("SystemDefaultForReal")  # или любая другая тема

    layout = [
        [sg.Text("Input CIF file:"), sg.Input(key="-INPUT-", size=(40, 1)),
         sg.FileBrowse(file_types=(("CIF files", "*.cif"), ("All files", "*.*")))],
        [sg.Text("Output folder:"), sg.Input(key="-OUTPUT-", size=(40, 1)),
         sg.FolderBrowse()],
        [sg.Text("HKL indices:"), sg.Input("0", key="-H-", size=(4, 1)),
         sg.Input("0", key="-K-", size=(4, 1)),
         sg.Input("1", key="-L-", size=(4, 1))],
        [sg.Text("Offset:"), sg.Input("0.0", key="-OFFSET-", size=(8, 1)),
         sg.Text("Mesh:"), sg.Input("4", key="-MESH-", size=(8, 1))],
        [sg.Text("Separation:"), sg.Input("36.0", key="-SEPARATION-", size=(8, 1)),
         sg.Text("Cutoff:"), sg.Input("3.0", key="-CUTOFF-", size=(8, 1))],
        [sg.Text("Approach:"),
         sg.Combo([1, 2, 3], default_value=1, key="-APPROACH-", readonly=True, size=(5, 1))],
        #[sg.Checkbox("Debug", default=False, key="-DEBUG-"),
        # sg.Checkbox("Force overwrite", default=False, key="-FORCE-")],
        [sg.Button("Run"), sg.Button("Cancel")],
        [sg.Output(size=(80, 10), key="-OUTPUT_LOG-")]  # вывод прогресса
    ]

    window = sg.Window("Layer Shifter", layout, icon=str(ICON_PATH))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "Run":
            try:
                # Собираем Namespace
                input_path = Path(values["-INPUT-"].strip())
                if not input_path.is_file():
                    sg.popup_error("Input CIF file does not exist.")
                    continue

                output_str = values["-OUTPUT-"].strip()
                output_dir = Path(output_str) if output_str else input_path.parent

                args = Namespace(
                    input=input_path,
                    output=output_dir,
                    hkl=[int(values["-H-"]), int(values["-K-"]), int(values["-L-"])],
                    offset=float(values["-OFFSET-"]),
                    mesh=int(values["-MESH-"]),
                    separation=float(values["-SEPARATION-"]),
                    approach=int(values["-APPROACH-"]),
                    cutoff=float(values["-CUTOFF-"]),
                    #debug=bool(values["-DEBUG-"]),
                    #force=bool(values["-FORCE-"]),
                    debug=False,
                    force=True,
                )

                # Запускаем обработку; сообщения print() будут появляться в окне
                print(f"Starting processing of {input_path.name}...")
                run(args)
                print("Processing completed successfully.")
                sg.popup("Success", "Processing completed.")
            except Exception as e:
                sg.popup_error(f"An error occurred:\n{e}")

    window.close()


if __name__ == "__main__":
    run_gui()