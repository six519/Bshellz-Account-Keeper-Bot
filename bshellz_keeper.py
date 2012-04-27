import socket, re

IRC_SERVER = "irc.freenode.net"
IRC_NICK = "bshellz_six519"
IRC_ROOM = "bshellz"
IRC_PORT = 6667
BSHELLZ_USER = "six519"

def sendMessage(sock, message):
	sock.send(message.encode())

def main():
	ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	quitting = False
	
	try:
		ircSocket.connect((IRC_SERVER, IRC_PORT))
		print "Connecting to: %s" % IRC_SERVER
		while True:
			buffer = ircSocket.recv(1024).decode("utf-8", 'replace')
			
			if re.search("Checking Ident", buffer):
				print "Authenticating your nickname: %s" % IRC_NICK
				sendMessage(ircSocket, "NICK %s\r\n" % IRC_NICK)
				sendMessage(ircSocket, "USER %s \"%s.ph\" \"%s\" :%s bobot\r\n" % (IRC_NICK, IRC_NICK, IRC_SERVER, IRC_NICK))
			elif re.search("Nickname is already in use|Erroneous Nickname|This nickname is registered", buffer):
				print "There's a problem on your nickname: %s" % IRC_NICK
				print "\nKeeper quits"
				quitting = True
			elif re.search("End of /MOTD command", buffer):
				print "Keeping your account: %s" % BSHELLZ_USER
				sendMessage(ircSocket, "JOIN #%s\r\n" % IRC_ROOM)
				sendMessage(ircSocket, "PRIVMSG #%s :!keep %s\r\n" % (IRC_ROOM, BSHELLZ_USER))
				sendMessage(ircSocket, "PRIVMSG #%s :Good day to all of you... :)\r\n" % IRC_ROOM)
				quitting = True
				
			if quitting:
				ircSocket = None
				break
		print "Successfully called keep command on the server\n\nKeeper quits"
		
	except Exception as err:
		print "An error occurred: %s" % err
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "\nKeeper quits"
