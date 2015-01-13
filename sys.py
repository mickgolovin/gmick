import SocketServer
import re
import MySQLdb

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
                data = bytes.decode(self.request[0].strip())
                socket = self.request[1]
                if (str(data).find("not in local ACL, by default reject")>=0):
                        ip = self.client_address[0]
                        mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', str(data), re.I).group()
                        print mac
                        db = MySQLdb.connect(host="localhost", user="root", passwd="superpassword", db="test", charset='utf8')
                        cursor = db.cursor()
                        sql_ins = """INSERT INTO test (ip, mac, time) VALUES ('%(ip)s', '%(mac)s', UNIX_TIMESTAMP())"""%{"ip":ip, "mac":mac}
                        cursor.execute(sql_ins)
                        sql_del = """DELETE FROM test WHERE time<UNIX_TIMESTAMP()-86400"""
                        cursor.execute(sql_del)
                        db.commit()
                        db.close()
                        

if __name__ == "__main__":
        try:
                server = SocketServer.UDPServer(("0.0.0.0",1235), SyslogUDPHandler)
                server.serve_forever(poll_interval=0.5)
        except (IOError, SystemExit):
                raise
        except KeyboardInterrupt:
                print ("Crtl+C Pressed. Shutting down.")
