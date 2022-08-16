from datetime import datetime
from json import loads, dumps
from random import randint
from PIL import Image
from io import BytesIO
from re import findall
from pathlib import Path
from urllib import request
from mutagen.mp3 import MP3
from time import sleep
from .Encryption import Encryption

__version__:str='‌'
__author__:str=''
__copyright__:str=''

class Clients:
	web = { "app_name"    : "Main", "app_version" : "4.0.7", "platform"    : "Web", "package"     : "web.rubika.ir", "lang_code"   : "fa" }
	android = { "app_name" : "Main", "app_version" : "2.9.8", "platform" : "Android", "package"     : "app.rbmain.a", "lang_code"   : "fa" }

class Bot:
	def __init__(self, auth,displayWelcome=True,):
		if len(auth) != 32: print('ش‍‌ن‍‌اس‍‌ه ی‍‌ا [auth] اک‍‌ان‍‌ت ش‍‌م‍‌ا, درس‍‌ت ن‍‌ی‍‌س‍‌ت ل‍‌ط‍‌ف‍‌ا ش‍‌ن‍‌اس‍‌ه اک‍‌ان‍‌ت خ‍‌ود را ب‍‌ه درس‍‌ت‍‌ی وارد ک‍‌ن‍‌ی‍‌د . . . !'); exit()
		if displayWelcome:
			text:str=f'{__author__}{__version__}{__copyright__}.\n🔻BoT is deletinG all MessaGe GroupinG and Channeling You . . .)\n\n'
			for char in text: print(char, flush=True, end=''); sleep(.1)
		self.auth = auth
		self.enc = Encryption(self.auth)

	def getChatsUpdate(self,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getChatsUpdates",
			"input":{
					"state":str(round(datetime.today().timestamp()) - 200),
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('chats')

	def sendChatActivity(self, object_guid, activity,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"sendChatActivity",
			"input":{
				"activity": activity,
				"object_guid": object_guid,
			},
			"client": Clients.web
		}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getChats(self, start_id=None,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getChats",
					"input":{
						"start_id":start_id,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('chats')

	@staticmethod
	def _parse(mode:str, text:str,):
		results = []
		if mode.upper() == "HTML":
			realText = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","")
			bolds = findall("<b>(.*?)</b>",text)
			italics = findall("<i>(.*?)</i>",text)
			monos = findall("<pre>(.*?)</pre>",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		elif mode.lower() == "markdown":
			realText = text.replace("**","").replace("__","").replace("`","")
			bolds = findall(r"\*\*(.*?)\*\*",text)
			italics = findall(r"\_\_(.*?)\_\_",text)
			monos = findall("`(.*?)`",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		return results

	def logout(self,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"logout",
					"input":{},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def forwardMessages(self, From, message_ids, to,):
		# from guid send to guid ...
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"forwardMessages",
					"input":{
						"from_object_guid": From,
						"message_ids": message_ids,
						"rnd": f"{randint(100000,999999999)}",
						"to_object_guid": to,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def banGroupMember(self, group_guid, user_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"banGroupMember",
					"input":{
						"group_guid": group_guid,
						"member_guid": user_id,
						"action":"Set"
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def requestSendFile(self, name, size, mime,):
		# mime = suffix
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"requestSendFile",
					"input":{
						"file_name": name,
						"mime": mime,
						"size": size,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data')

	def uploadFile(self, file_byte ,access_hash_send ,file_id ,url):
		if len(file_byte) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(file_byte)),
				'file-id':str(file_id),
				'access-hash-send':access_hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = request.urlopen(request.Request(url, data=file_byte, headers=h)).read().decode('utf-8')
					print(j)
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = round(len(file_byte) / 131072 + 1)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = request.urlopen(request.Request(url, data=file_byte[k:k + 131072],headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':access_hash_send,
								'total-part':str(t),
								'part-number':str(i)
							})).read().decode('utf-8')
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(file_byte) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = request.urlopen(request.Request(url, data=file_byte[k:],headers={
								'auth':self.auth,
								'chunk-size':str(len(file_byte[k:])),
								'file-id':file_id,
								'access-hash-send':access_hash_send,
								'total-part':str(t),
								'part-number':str(i)
							})).read().decode('utf-8')
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(file_byte) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p

	@staticmethod
	def getThumbInline(image_bytes:bytes):
		try:
			im = Image.open(BytesIO(image_bytes))
			width, height = im.size
			if height > width:
				new_height = 40
				new_width  = round(new_height * width / height)
			else:
				new_width  = 40
				new_height = round(new_width * height / width)
			im = im.resize((new_width, new_height), Image.ANTIALIAS)
			changed_image = BytesIO()
			im.save(changed_image, format='PNG')
			changed_image = changed_image.getvalue()
			return b64encode(changed_image)
		except: pass

	@staticmethod
	def getImageSize(image_bytes:bytes):
		im = Image.open(BytesIO(image_bytes))
		width, height = im.size
		return [width , height]

	def sendMessage(self, chat_id, text, metadata=[], parse_mode=None, message_id=None):
		inData = {
				"method":"sendMessage",
				"input":{
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"text":text,
					"reply_to_message_id":message_id
				},
				"client": Clients.web
			}
		if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
		if parse_mode != None :
			inData["input"]["metadata"] = {"meta_data_parts":Bot._parse(parse_mode, text)}
			inData["input"]["text"] = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else text.replace("**","").replace("__","").replace("`","")
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def editMessage(self, message_id, object_guid, newText,metadata=[],parse_mode=None,):
		inData = {
				"method":"editMessage",
				"input":{
					"message_id": message_id,
					"object_guid": object_guid,
					"text": newText,
					},
				"client": Clients.web
			}
		if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
		if parse_mode != None :
			inData["input"]["metadata"] = {"meta_data_parts":Bot._parse(parse_mode, newText)}
			inData["input"]["text"] = newText.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else newText.replace("**","").replace("__","").replace("`","")
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def unbanGroupMember(self, group_guid, user_id):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"banGroupMember",
					"input":{
						"group_guid": group_guid,
						"member_guid": user_id,
						"action":"Unset"
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def deleteMessages(self, object_guid, message_ids=[]):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"deleteMessages",
					"input":{
						"object_guid": object_guid,
						"message_ids":message_ids,
						"type":"Global",
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getUserInfo(self, object_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getUserInfo",
					"input":{
						"user_guid":object_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getGroupAdminMembers(self, object_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getGroupAdminMembers",
					"input":{
						"group_guid": object_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def addChannelMembers(self, channel_guid, user_ids=[]):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"addChannelMembers",
					"input":{
						"channel_guid": channel_guid,
						"member_guids": user_ids,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def setGroupDefaultAccess(self, group_guid, access_list=[]):
		#request with api v 4
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"4","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setGroupDefaultAccess",
					"access_list": access_list,
					"group_guid": group_guid,
					"client": Clients.android
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getGroupLink(self, group_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getGroupLink",
					"input":{
						"group_guid":group_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('join_link')

	def changeGroupLink(self, group_guid):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setGroupLink",
					"input":{
						"group_guid":group_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def setGroupTimer(self, group_guid, time,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"editGroupInfo",
					"input":{
						"group_guid":group_guid,
						"slow_mode": time,
						"updated_parameters":["slow_mode"],
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def sendMusic(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, time, size ,music_performer=None,text=None, message_id=None):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"sendMessage",
					"input":{
						"object_guid":chat_id,
						"rnd":f"{randint(100000,900000)}",
						"reply_to_message_id":message_id,
						"text":text,
						"file_inline":{
							"dc_id":str(dc_id),
							"file_id":str(file_id),
							"type":"Music",
							"music_performer":'@BLOW_JUB_com' if music_performer==None else music_performer,
							"file_name":file_name,
							"size":size,
							"mime":mime,
							'time': time,
							'width': 0.0,
							'height':0.0,
							"access_hash_rec":access_hash_rec,
						}},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def addChannel(self, type, channel_name,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"addChannel",
					"input":{
						"channel_type":type,
						"title":channel_name,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def seenChats(self, seenList,):
		# seenList must be a dict , keys are object guids and values are last message’s id, {"guid":"msg_id"}
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"addChannel",
					"input":{
						"seen_list": seenList,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def updateChannelUsername(self, channel_guid, username,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"updateChannelUsername",
					"input":{
						"channel_guid": channel_guid,
						"username": username,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def deleteGroupAdmin(self, group_guid, user_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setGroupAdmin",
					"input":{
						"group_guid": group_guid,
						"action": "UnsetAdmin",
						"member_guid": user_id,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def pin(self, object_guid, message_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setPinMessage",
					"input":{
						"action":"Pin",
						"message_id": message_id,
						"object_guid": object_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def unpin(self, object_guid, message_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setPinMessage",
					"input":{
						"action":"Unpin",
						"message_id": message_id,
						"object_guid": object_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def joinGroup(self, link,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"joinGroup",
					"input":{
						"hash_link": link.split("/")[-1],
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def groupPreviewByJoinLink(self, link,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"groupPreviewByJoinLink",
					"input":{
						"hash_link": link.split("/")[-1],
						},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def leaveGroup(self, group_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"leaveGroup",
					"input":{
						"group_guid": group_guid,
						},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def deleteNoAccessGroupChat(self, group_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"deleteNoAccessGroupChat",
					"input":{
						"group_guid": group_guid,
					},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def block(self, user_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setBlockUser",
					"input":{
						"action":"Block",
						"user_guid": user_guid, },
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def unBlock(self, user_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setBlockUser",
					"input":{
						"action":"Unblock",
						"user_guid": user_guid, },
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getGroupInfo(self, group_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": group_guid,
						}, "client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getChannelInfo(self, channel_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getChannelInfo",
					"input":{
						"channel_guid": channel_guid,
						},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getMessages(self, chat_id,middle_message_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getMessagesInterval",
					"input":{
						"object_guid":chat_id,
						"middle_message_id":middle_message_id,
						},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('messages')

	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"sendMessage",
					"input":{
						"object_guid":chat_id,
						"rnd":f"{randint(100000,900000)}",
						"reply_to_message_id":message_id,
						"text":text,
						"file_inline":{
							"dc_id":str(dc_id),
							"file_id":str(file_id),
							"type":"Image",
							"file_name":file_name,
							"size":size,
							"mime":mime,
							"access_hash_rec":access_hash_rec,
							'thumb_inline':thumb_inline,
							'width':width,
							'height':height,
						}},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def sendFile(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, size, text=None, message_id=None):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"sendMessage",
					"input":{
						"object_guid":chat_id,
						"rnd":f"{randint(100000,900000)}",
						"reply_to_message_id":message_id,
						"text":text,
						"file_inline":{
							"dc_id":str(dc_id),
							"file_id":str(file_id),
							"type":"File",
							"file_name":file_name,
							"size":size,
							"mime":mime,
							"access_hash_rec":access_hash_rec,
						}},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def myStickerSet(self,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
		"method":"getMyStickerSets",
		"input":{},
		"client": Clients.web
		}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data')

	def startVoiceChat(self, chat_id, on="Group"):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":f"create{on}VoiceChat",
				"input":{
					f"{on.lower()}_guid":chat_id,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def editVoiceChat(self, chat_id,voice_chat_id, title, on="Group"):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":f"set{on}VoiceChatSetting",
				"input":{
					f"{on.lower()}_guid":chat_id,
					"voice_chat_id" : voice_chat_id,
					"title" : title ,
					"updated_parameters": ["title"],
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getMessagesUpdates(self, chat_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getMessagesUpdates",
				"input":{
					"object_guid":chat_id,
					"state":str(round(datetime.today().timestamp()) - 200),
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def deleteAvatar(self, guid, avatar_id,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"deleteAvatar",
				"input":{
					"object_guid":guid,
					"avatar_id":avatar_id,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getMessagesInfo(self, chat_id, message_ids=[]):
			return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getMessagesByID",
				"input":{
					"object_guid": chat_id,
					"message_ids": message_ids,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('messages')

	def deleteChatHistory(self, chat_id, last_message_id):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"deleteChatHistory",
				"input":{
					"last_message_id": last_message_id,
					"object_guid": chat_id,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def download(self, dl="message",save=False,**kwargs):
		result = b""
		if dl == "message":
			message = kwargs["message"]
			if type(message) != dict:
				message = Bot(self.auth).getMessagesInfo(kwargs["chat_id"], [str(message)])[0]
			fileID = str(message["file_inline"]["file_id"])
			size = message["file_inline"]["size"]
			dc_id = str(message["file_inline"]["dc_id"])
			accessHashRec = message["file_inline"]["access_hash_rec"]
			filename = message["file_inline"]["file_name"]
		else :
			fileID = str(kwargs.get("fileID"))
			size = kwargs.get("size")
			dc_id = str(kwargs.get("dc_id"))
			accessHashRec = kwargs.get("accessHashRec")

		header = {
			'auth':self.auth,
			'file-id':fileID,
			'access-hash-rec':accessHashRec
		}
		server = "https://messenger"+dc_id+".iranlms.ir/GetFile.ashx"
		if size <= 131072:
			header["start-index"], header["last-index"] = "0",str(size)
			while True:
				try:
					result += get(url=server,headers=header).content
					break
				except Exception as e:
					print (e)
					continue
		else:
			lastnow = 0
			lastlast = 131072
			while True:
				try:
					if lastnow <= 131072:
						header["start-index"], header["last-index"] = "0", str(size)
						result += get(url=server,headers=header).content
					else:
						for i in range(0,size,131072):
							header["start-index"], header["last-index"] = str(i), str(i+131072 if i+131072 <= size else size)
							result += get(url=server,headers=header).content
					break
				except Exception as e:
					print(e)

		if save:
			with open(kwargs.get("saveAs") or f"{filename}","wb") as file: file.write(result)
		else:
			return result

	def getGroupAllMembers(self, chat_id, start_id=None):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getGroupAllMembers",
				"input":{
					"group_guid": chat_id,
					"start_id": start_id,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('in_chat_members')

	def setGroupAdmin(self, chat_id, user_id, access_list=[]):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"setGroupAdmin",
				"input":{
					"group_guid": chat_id,
					"access_list": access_list,
					"action": "SetAdmin",
					"member_guid": user_id,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def sendVoice(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"sendMessage",
					"input":{
						"object_guid":chat_id,
						"rnd":f"{randint(100000,900000)}",
						"reply_to_message_id":message_id,
						"text":text,
						"file_inline":{
							"dc_id":str(dc_id),
							"file_id":str(file_id),
							"type":"Voice",
							"file_name":file_name,
							"size":size,
							"mime":mime,
							"access_hash_rec":access_hash_rec,
							'time':duration,
						}},
					"client": Clients.web
				}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getChannelMembers(self, channel_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getChannelAllMembers",
				"input":{
					"channel_guid": channel_guid,
					'search_text': None,
					'start_id': None,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getChannelLink(self, channel_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getChannelLink",
				"input":{
					"channel_guid": channel_guid,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def finishVoiceChat(self, chat_id, voice_chat_id, on="Group",):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":f"discard{on}VoiceChat",
				"input":{
					f"{on.lower()}_guid":chat_id,
					"voice_chat_id" : voice_chat_id,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getAvatars(self,guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getAvatars",
				"input":{
					"object_guid":guid,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def setChannelLink(self, channel_guid,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"setChannelLink",
				"input":{
					"channel_guid": channel_guid,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def searchGlobalObjects(self, search_text,):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"searchGlobalObjects",
				"input":{
					"search_text": search_text,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get('data').get('objects')

	def addGroupMembers(self, group_guid, user_ids):
		return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"addGroupMembers",
				"input":{
					"group_guid": group_guid,
					"member_guids": user_ids,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))

	def getInfoByUsername(self, username,):
		try:
			if '@' in username: username = username.replace('@', '')
			else: username = username
			return loads(self.enc.decrypt(loads(request.urlopen(request.Request('https://messengerg2c64.iranlms.ir/', data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getObjectByUsername",
				"input":{
					"username": username,
				},
				"client": Clients.web
			}))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
		except: pass

class Uploader:
	def __init__(self, auth,):
		self.auth=Bot(auth, displayWelcome=False,)

	def sendPhoto(self,object_guid, url_or_file, caption=None, message_id=None,):
		if url_or_file.startswith('http'):
			file_name='BLOW_JUB'+str(randint(10000, 999999999))+'.png'
			byte=request.urlopen(request.Request(url_or_file)).read()
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile(file_name, len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.uploadFile(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, file_name, len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,text=caption, message_id=message_id)
		else:
			byte=open(url_or_file, 'rb').read()
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile('BLOW_JUB.png', len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.uploadFile(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, 'BLOW_JUB.png', len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height, caption, message_id)

	def sendDocument(self, object_guid, url_or_file,suffix=None, file_name=None,caption=None, message_id=None):
		if url_or_file.startswith('http'):
			if file_name==None:
				file_name='BLOW_JUB'+str(randint(10000, 999999999))+'.'+suffix
			else:
				file_name=file_name+'.'+suffix
			byte=request.urlopen(request.Request(url_or_file)).read()
			rsf=self.auth.requestSendFile(file_name, len(byte), suffix[1:]) # rsf = request send File
			if rsf!='many_request':
				access = self.auth.uploadFile(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendFile(object_guid,rsf['id'] , suffix, rsf['dc_id'] , access, file_name, len(byte), text=caption,message_id=message_id,)
		else:
			suffix = Path(url_or_file).suffix
			if file_name==None:
				file_name='BLOW_JUB'+str(randint(10000, 999999999))+suffix
			else:
				file_name=file_name+suffix
			byte=open(url_or_file, 'rb').read()
			rsf=self.auth.requestSendFile(file_name, len(byte), suffix[1:]) # rsf = request send File
			if rsf!='many_request':
				access = self.auth.uploadFile(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendFile(object_guid,rsf['id'] , suffix[1:], rsf['dc_id'] , access, file_name, len(byte), text=caption,message_id=message_id,)

	def sendMusic(self,chat_id, url_or_file, file_name=None,caption=None, message_id=None,):
		if url_or_file.startswith('http'):
			byte=request.urlopen(request.Request(url_or_file)).read()
			rsf=self.auth.requestSendFile('BLOW_JUB.mp3' if file_name==None else file_name+'.mp3', len(byte), 'mp3') # rsf = Request Send File
			if rsf!='many_request':
				access = self.auth.uploadFile(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				duration=BytesIO()
				duration.write(byte)
				duration.seek(0)
				duration = MP3(duration).info.length
				self.auth.sendMusic(chat_id,rsf['id'] , 'mp3', rsf['dc_id'] , access, 'BLOW_JUB.mp3' if file_name==None else file_name+'.mp3', duration,len(byte),music_performer=None,text=caption,message_id=message_id)
			else: raise Exception('send File Error : You have submitted too many requests.')
		else:
			byte=open(url_or_file, 'rb').read()
			suffix=Path(url_or_file).suffix
			rsf=self.auth.requestSendFile(f'BLOW_JUB{suffix[1:]}' if file_name==None else file_name, len(byte), suffix[1:]) # rsf = Request Send File
			if rsf!='many_request':
				access = self.auth.uploadFile(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendMusic(chat_id,rsf['id'] , suffix[1:], rsf['dc_id'] , access, f'BLOW_JUB{suffix}' if file_name==None else file_name+suffix, MP3(url_or_file).info.length,len(byte),music_performer=None,text=caption,message_id=message_id)
			else: raise Exception('send File Error : You have submitted too many requests.')