import cx_Freeze
import glob

executables = [cx_Freeze.Executable("game.py", base="Win32GUI", icon="assets/icon.ico")]

excludes = {"excludes": ["tkinter", "pytz", "numpy", "scipy", "email", "html", "http", "json", "lib2to3", "multiprocessing", "test", "unittest", "urllib", "xmlrpc"]}

a = glob.glob("*.png")
a.extend(glob.glob("*.ogg"))
a.extend(glob.glob("*.ttf"))

cx_Freeze.setup(
    name="A City Minute",
    options={"build_exe": {"packages":["pygame"],
                           "excludes":excludes["excludes"],
                           "include_files": ["assets"]}},
    executables = executables,
    version = "1.0"
    )