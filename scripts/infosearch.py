import sys
import os
import subprocess
import shutil

def usage():
    print("Usage:")
    print(f"{sys.argv[0]} {{path to extracted file system of firmware}} "
          f"{{optional: name of the file to store results - defaults to firmwalker.txt}}")
    print("Example: python {0} linksys/fmk/rootfs/".format(sys.argv[0]))
    sys.exit(1)

def msg(message):
    data = message.split("\n")
    tmp = list(set(data))
    message = "\n".join(tmp)[1:]
    with open(FILE, "a") as file:
        file.write(message + "\n")
    print(message)

def get_array(file):
    array = []
    file = "./" + file
    with open(file, "r") as file:
        for line in file:
            array.append(line.strip())
    return array

def remove_file(file):
    if os.path.exists(file) and os.path.isfile(file) and not os.path.islink(file):
        os.remove(file)

if __name__ == "__main__":
    # Check for arguments
    # print(sys.argv)
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        usage()
        exit(0)

    # Set variables
    FIRMDIR = sys.argv[1]
    if len(sys.argv) == 3:
        FILE = sys.argv[2]
    else:
        FILE = "firmwalker.txt"

    # Remove previous file if it exists, is a file and doesn't point somewhere
    remove_file(FILE)

    # Perform searches
    msg("***Firmware Directory***")
    msg(FIRMDIR)
    msg("***Search for password files***")
    passfiles = get_array("data/passfiles")
    for passfile in passfiles:
        msg("##################################### " + passfile)
        text = subprocess.run(["find", FIRMDIR, "-name", passfile, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for Unix-MD5 hashes***")
    text = subprocess.run(["egrep", "-sro", "'\\$1\\$\\w{8}\\S{23}'", FIRMDIR, "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
    msg(text)
    msg("")

    if os.path.isdir(os.path.join(FIRMDIR, "etc/ssl")):
        msg("***List etc/ssl directory***")
        text = subprocess.run(["ls", "-l", os.path.join(FIRMDIR, "etc/ssl"), "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
    msg("")

    msg("***Search for SSL related files***")
    sslfiles = get_array("data/sslfiles")
    for sslfile in sslfiles:
        msg("##################################### " + sslfile)
        text = subprocess.run(["find", FIRMDIR, "-name", sslfile, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        certfiles = subprocess.check_output(["find", FIRMDIR, "-name", sslfile]).decode().strip().split("\n")
        for certfile in certfiles:
            serialno = subprocess.run(["openssl", "x509", "-in", certfile, "-serial", "-noout"], capture_output=True, text=True).stdout.strip()
            if len(serialno.split("=")) > 1:
                serialnoformat = "ssl.cert.serial:" + serialno.split("=")[1]
                if shutil.which("shodan"):
                    shocount = subprocess.run(["shodan", "count", serialnoformat], capture_output=True, text=True).stdout.strip()
                    if int(shocount) > 0:
                        msg("################# Certificate serial # found in Shodan ####################")
                        msg(certfile[len(FIRMDIR) + 1:])
                        msg(serialno)
                        msg("Number of devices found in Shodan =" + shocount)
                        with open(certfile, "r") as file:
                            msg(file.read())
                        msg("###########################################################################")
                else:
                    msg("Shodan cli not found.")
        msg("")

    msg("***Search for SSH related files***")
    sshfiles = get_array("data/sshfiles")
    for sshfile in sshfiles:
        msg("##################################### " + sshfile)
        text = subprocess.run(["find", FIRMDIR, "-name", sshfile, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for files***")
    files = get_array("data/files")
    for file in files:
        msg("##################################### " + file)
        text = subprocess.run(["find", FIRMDIR, "-name", file, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for database related files***")
    dbfiles = get_array("data/dbfiles")
    for dbfile in dbfiles:
        msg("##################################### " + dbfile)
        text = subprocess.run(["find", FIRMDIR, "-name", dbfile, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for shell scripts***")
    msg("##################################### shell scripts")
    text = subprocess.run(["find", FIRMDIR, "-name", "*.sh", "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
    msg(text)
    msg("")

    msg("***Search for other .bin files***")
    msg("##################################### bin files")
    text = subprocess.run(["find", FIRMDIR, "-name", "*.bin", "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
    msg(text)
    msg("")

    msg("***Search for patterns in files***")
    patterns = get_array("data/patterns")
    for pattern in patterns:
        msg("-------------------- " + pattern + " --------------------")
        text = subprocess.run(["grep", "-lsirnw", FIRMDIR, "-e", pattern, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for web servers***")
    msg("##################################### search for web servers")
    webservers = get_array("data/webservers")
    for webserver in webservers:
        msg("##################################### " + webserver)
        text = subprocess.run(["find", FIRMDIR, "-name", webserver, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for important binaries***")
    msg("##################################### important binaries")
    binaries = get_array("data/binaries")
    for binary in binaries:
        msg("##################################### " + binary)
        text = subprocess.run(["find", FIRMDIR, "-name", binary, "|", "cut", "-c" + str(len(FIRMDIR) + 1) + "-", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
        msg(text)
        msg("")

    msg("***Search for ip addresses***")
    msg("##################################### ip addresses")
    text = subprocess.run(["grep", "-sRIEho", r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", "--exclude-dir=dev", FIRMDIR, "|", "sort", "|", "uniq", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
    msg(text)
    msg("")

    msg("***Search for urls***")
    msg("##################################### urls")
    text = subprocess.run(["grep", "-sRIEoh", "(http|https)://[^/\"]+", "--exclude-dir=dev", FIRMDIR, "|", "sort", "|", "uniq", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
    msg(text)
    msg("")

    msg("***Search for emails***")
    msg("##################################### emails")
    text = subprocess.run(["grep", "-sRIEoh", r"([[:alnum:]_.-]+@[[:alnum:]_.-]+?\.[[:alpha:].]{2,6})", "$@", "--exclude-dir=dev", FIRMDIR, "|", "sort", "|", "uniq", "|", "tee", "-a", FILE], capture_output=True, text=True).stdout.strip()
    msg(text)
