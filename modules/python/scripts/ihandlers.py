import logging
import os
import imp

from dionaea.core import g_dionaea

# service imports
import dionaea.tftp
import dionaea.cmd
import dionaea.emu
import dionaea.store
import dionaea.test
import dionaea.ftp

logger = logging.getLogger('ihandlers')
logger.setLevel(logging.DEBUG)


# reload service imports
#imp.reload(dionaea.tftp)
#imp.reload(dionaea.ftp)
#imp.reload(dionaea.cmd)
#imp.reload(dionaea.emu)
#imp.reload(dionaea.store)

# global handler list
# keeps a ref on our handlers
# allows restarting
global g_handlers



def start():
	global g_handlers
	g_handlers = []

	if "ftpdownload" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.ftp
		g_handlers.append(dionaea.ftp.ftpdownloadhandler('dionaea.download.offer'))

	if "tftpdownload" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		g_handlers.append(dionaea.tftp.tftpdownloadhandler('dionaea.download.offer'))

	if "emuprofile" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		g_handlers.append(dionaea.emu.emuprofilehandler('dionaea.module.emu.profile'))

	if "cmdshell" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		g_handlers.append(dionaea.cmd.cmdshellhandler('dionaea.service.shell.*'))

	if "store" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		g_handlers.append(dionaea.store.storehandler('dionaea.download.complete'))

	if "uniquedownload" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		g_handlers.append(dionaea.test.uniquedownloadihandler('dionaea.download.complete.unique'))

	if "surfids" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.surfids
		g_handlers.append(dionaea.surfids.surfidshandler('*'))

	if "logsql" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.logsql
		g_handlers.append(dionaea.logsql.logsqlhandler("*"))

	if "p0f" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.p0f
		g_handlers.append(dionaea.p0f.p0fhandler(g_dionaea.config()['modules']['python']['p0f']['path']))

	if "logxmpp" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.logxmpp
		from random import choice
		import string
		for client in g_dionaea.config()['modules']['python']['logxmpp']:
			conf = g_dionaea.config()['modules']['python']['logxmpp'][client]
			if 'resource' in conf:
				resource = conf['resource']
			else:
				resource = ''.join([choice(string.ascii_letters) for i in range(8)])
			print("client %s \n\tserver %s:%s username %s password %s resource %s muc %s\n\t%s" % (client, conf['server'], conf['port'], conf['username'], conf['password'], resource, conf['muc'], conf['config']))
			x = dionaea.logxmpp.logxmpp(conf['server'], int(conf['port']), conf['username'], conf['password'], resource, conf['muc'], conf['config'])
			g_handlers.append(x)

	if "nfq" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.nfq
		g_handlers.append(dionaea.nfq.nfqhandler())


	if "virustotal" in g_dionaea.config()['modules']['python']['ihandlers']['handlers']:
		import dionaea.virustotal
		g_handlers.append(dionaea.virustotal.virustotalhandler())


def stop():
	global g_handlers
	for i in g_handlers:
		logger.debug("deleting %s" % str(i))
		del i
	del g_handlers

