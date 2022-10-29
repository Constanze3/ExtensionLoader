import subprocess
import os


def saveExtensions(fileName="extensions.txt"):
    extensions = subprocess.check_output(
        "code --list-extensions", shell=True).decode()
    with open(fileName, "w") as file:
        file.write(extensions)


def deleteExtensions(fileName="", logDeletedExtensions=True):
    defaultLog = "deleted.txt"
    useDefaultLog = fileName == ""
    log = defaultLog if useDefaultLog else fileName
    saveExtensions(log)
    executeOnAllExtensions("--uninstall-extension", log)
    if not logDeletedExtensions and useDefaultLog:
        os.remove(defaultLog)


def loadExtensions(extensionsFile="extensions.txt"):
    executeOnAllExtensions("--install-extension", extensionsFile)


def executeOnAllExtensions(command, extensionsFile):
    with open(extensionsFile, "r") as file:
        for line in file:
            extension = line.strip()
            try:
                subprocess.run(["code", command, extension],
                            shell=True,
                            env=os.environ,
                            check=True)
            except subprocess.CalledProcessError:
                print("extension '" + extension + "' doesn't exist")


action = input("What to do (save, load, delete) ? ")

if action == "save":
    saveExtensions()
elif action == "load":
    loadExtensions()
elif action == "delete":
    deleteExtensions()
