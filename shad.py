from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode , urlsafe_b64decode
from datetime import datetime
from json import loads, dumps
from requests import post, get
from random import randint
from PIL import Image
from io import BytesIO
from re import findall
from pathlib import Path

class Encryption:
    def __init__(self, auth,):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        return b64encode(enc).decode('UTF-8')

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(urlsafe_b64decode(text.encode('UTF-8')))
        return unpad(dec, AES.block_size).decode('UTF-8')

class Clients:
	web = { "app_name"    : "Main", "app_version" : "3.2.2", "platform"    : "Web", "package"     : "web.shad.ir", "lang_code"   : "fa" }
	android = { "app_name" : "Main", "app_version" : "2.9.8", "platform" : "Android", "package"     : "ir.medu.shad", "lang_code"   : "fa" }

class Bot:
	def __init__(self, auth,):
		if len(auth) != 32: print('Your account AUTH ID is incorrect, please check and then try again.'); exit()
		print('This library was created by Shayan Heydari\nSetting up codes ...\n\n\n')
		self.auth = auth
		self.enc = Encryption(self.auth)

	def getChatsUpdate(self,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getChatsUpdates", "input":{ "state": str(round(datetime.today().timestamp()) - 1000), }, "client": Clients.web }))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc"))).get('data').get('chats')

	def sendChatActivity(self, object_guid, activity,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"sendChatActivity",
				"input":{
					"activity": activity,
					"object_guid": object_guid
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc")))

	def getChats(self, start_id=None,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getChats",
			"input":{
				"start_id":start_id
			},
			"client": Clients.android
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"])).get('data').get('chats')

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
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"logout",
			"input":{},
			"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def forwardMessages(self, From, message_ids, to):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"forwardMessages",
				"input":{
					"from_object_guid": From,
					"message_ids": message_ids,
					"rnd": f"{randint(100000,999999999)}",
					"to_object_guid": to
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def banGroupMember(self, group_guid, user_id):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"banGroupMember",
			"input":{
				"group_guid": group_guid,
				"member_guid": user_id,
				"action":"Set"
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/')

	def requestSendFile(self, name, size, mime,):
		# mime = suffix
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"requestSendFile",
				"input":{
				"file_name": name,
				"mime": mime,
				"size": size
				},
				"client": Clients.web
				}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))["data"]
		except: return 'Error requestSendFile'

	def fileUpload(self, bytef ,hash_send ,file_id ,url):
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = round(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
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
		try:
			im = Image.open(BytesIO(image_bytes))
			width, height = im.size
			return [width , height]
		except: pass

	def sendMessage(self, chat_id, text, metadata=[], parse_mode=None, message_id=None):
		try:
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
	
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def editMessage(self, message_id, object_guid, newText):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"editMessage",
			"input":{
				"message_id": message_id,
				"object_guid": object_guid,
				"text": newText
			},
			"client":Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/')

	def unbanGroupMember(self, group_guid, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client": Clients.android,
			"input":{
				"group_guid": group_guid,
				"member_guid": user_id,
				"action":"Unset"
			},
			"method":"banGroupMember"
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def deleteMessages(self, object_guid, message_ids=[]):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"deleteMessages",
				"input":{
					"object_guid": object_guid,
					"message_ids":message_ids,
					"type":"Global"
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def getUserInfo(self, object_guid):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getUserInfo",
			"input":{
				"user_guid":object_guid
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def getGroupAdminMembers(self, object_guid):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"client": Clients.web,
				"input":{
					"group_guid": object_guid
				},
				"method":"getGroupAdminMembers"
			}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc")))
		except: pass
	
	def addChannelMembers(self, channel_guid, user_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addChannelMembers",
			"input":{
				"channel_guid": channel_guid,
				"member_guids": user_ids
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def setGroupDefaultAccess(self, group_guid, access_list):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": Clients.web,
			"data_enc": self.enc.encrypt(dumps({
				"access_list": access_list,
				"group_guid": group_guid
			})),
			"method": "setGroupDefaultAccess"
		}, url='https://shadmessenger78.iranlms.ir/')

	def getGroupLink(self, chat_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getGroupLink",
				"input":{
					"group_guid":chat_id
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc"))).get("data").get("join_link")
		except: pass

	def changeGroupLink(self, group_guid):
		try:
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": Clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"group_guid": group_guid
				})),
				"method":"setGroupLink",
			},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def setGroupTimer(self, object_guid, time):
		try:
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": Clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"group_guid": object_guid,
					"slow_mode": time,
					"updated_parameters":["slow_mode"]
				})),
				"method":"editGroupInfo"
			},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def addChannel(self, type, channel_name):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"addChannel",
				"input":{
					"channel_type": type,
					"title": channel_name
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def seenChats(self, seenList):
		# seenList must be a dict , keys are object guids and values are last message’s id, {"guid":"msg_id"}
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"seenChats",
			"input":{
				"seen_list": seenList
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def updateChannelUsername(self, channel_guid, username,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"updateChannelUsername",
			"input":{
				"channel_guid": channel_guid,
				"username": username
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def deleteGroupAdmin(self, group_guid, user_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"setGroupAdmin",
				"input":{
					"group_guid": group_guid,
					"action": "UnsetAdmin",
					"member_guid": user_id
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def pin(self, object_guid, message_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version": "4", "auth": self.auth, "client": Clients.android,
				 "data_enc": self.enc.encrypt(dumps({
				 	"action":"Pin",
				 	"message_id": message_id,
				 	"object_guid": object_guid
				 })),
				"method": "setPinMessage"
			},url='https://shadmessenger78.iranlms.ir/')))
		except: pass

	def unpin(self, chat_id, message_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version": "4", "auth": self.auth, "client": Clients.android,
				 "data_enc": self.enc.encrypt(dumps({
				 	"action":"Unpin",
				 	"message_id": message_id,
				 	"object_guid": chat_id
				 })),
				"method": "setPinMessage"
			},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def joinGroup(self, link):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"joinGroup",
				"input":{
					"hash_link": link.split("/")[-1]
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def groupPreviewByJoinLink(self, link):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"groupPreviewByJoinLink",
				"input":{
					"hash_link": link.split("/")[-1]
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))["data"]
		except: pass

	def leaveGroup(self, group_guid):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"leaveGroup",
				"input":{
					"group_guid": group_guid
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def deleteNoAccessGroupChat(self, group_guid,):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"deleteNoAccessGroupChat",
				"input":{
					"group_guid": group_guid
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def block(self, chat_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"setBlockUser",
				"input":{
					"action": "Block",
					"user_guid": chat_id
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def unBlock(self, chat_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"setBlockUser",
				"input":{
					"action": "Unblock",
					"user_guid": chat_id
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def getGroupInfo(self, group_guid,):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": group_guid,
					},
					"client": Clients.web
			}))}, url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def getChannelInfo(self, channel_guid,):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getChannelInfo",
					"input":{
						"channel_guid": channel_guid,
					},
					"client": Clients.web
			}))}, url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def getMessages(self, chat_id,min_id,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesInterval",
			"input":{
				"object_guid":chat_id,
				"middle_message_id":min_id
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc"))).get("data").get("messages")

	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
		return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
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
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))

	def sendFile(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, size, text=None, message_id=None):
		try:
			return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"sendMessage",
			"input":{
			"object_guid":chat_id,
			"rnd":f"{randint(100000,900000)}",
			"text":text,
			"reply_to_message_id":message_id,
			"file_inline":{
			"dc_id":str(dc_id),
			"file_id":str(file_id),
			"type":"File",
			"file_name":file_name,
			"size":size,
			"mime":mime,
			"access_hash_rec":access_hash_rec
			}}, "client":Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').text)['data_enc']))
		except: pass

	def myStickerSet(self,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMyStickerSets",
			"input":{},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc"))).get("data")

	def startVoiceChat(self, chat_id, on="Group"):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":f"create{on}VoiceChat",
			"input":{
				f"{on.lower()}_guid":chat_id,
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def editVoiceChat(self, chat_id,voice_chat_id, title, on="Group"):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":f"set{on}VoiceChatSetting",
			"input":{
				f"{on.lower()}_guid":chat_id,
				"voice_chat_id" : voice_chat_id,
				"title" : title ,
				"updated_parameters": ["title"]
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def getMessagesUpdates(self, chat_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getMessagesUpdates",
				"input":{
					"object_guid":chat_id,
					"state":str(round(datetime.today().timestamp()) - 200)
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc"))).get("data").get("updated_messages")
		except: pass

	def deleteAvatar(self, myguid, avatar_id):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"deleteAvatar",
				"input":{
					"object_guid":myguid,
					"avatar_id":avatar_id
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: return 'error delete avatar'

	def editProfile(self, **kwargs):
		if "username" in list(kwargs.keys()):
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": Clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"username": kwargs.get("username"),
					"updated_parameters":["username"]
				})),
				"method":"updateUsername"
			},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
			kwargs = kwargs.pop("username")

		if len(list(kwargs.keys())) > 0:
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": Clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"first_name": kwargs.get("first_name"),
					"last_name": kwargs.get("last_name"),
					"bio": kwargs.get("bio"),
					"updated_parameters":list(kwargs.keys())
				})),
				"method":"updateProfile"
			},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def getMessagesInfo(self, chat_id, message_ids=[]):
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getMessagesByID",
				"input":{
					"object_guid": chat_id,
					"message_ids": message_ids
				},
				"client": Clients.web
			}))}, url='https://shadmessenger78.iranlms.ir/').json()["data_enc"])).get("data").get("messages")

	def deleteChatHistory(self, chat_id, lastMessageId):
		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": Clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"object_guid": chat_id,
				"last_message_id": lastMessageId
			})),
			"method": "deleteChatHistory"
		}, url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

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
		try:
			return loads(self.enc.decrypt(post(json={
				"api_version":"5",
					"auth": self.auth,
					"data_enc": self.enc.encrypt(dumps({
						"method":"getGroupAllMembers",
						"input":{
							"group_guid": chat_id,
							"start_id": start_id
						},
						"client": Clients.web
				}))
			}, url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def setGroupAdmin(self, chat_id, user_id, access_list=[]):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"setGroupAdmin",
				"input":{
					"group_guid": chat_id,
					"access_list": access_list,
					"action": "SetAdmin",
					"member_guid": user_id
				},
				"client": Clients.android
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: return 'error setAdmin'

	def sendVoice(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
		try:
			return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"sendMessage",
			"input":{
			"object_guid":chat_id,
			"rnd":f"{randint(100000,900000)}",
			"text":text,
			"reply_to_message_id":message_id,
			"file_inline":{
			"dc_id":str(dc_id),
			"file_id":str(file_id),
			"type":"Voice",
			"file_name":file_name,
			"size":size,
			"mime":mime,
			"access_hash_rec":access_hash_rec,
			'time':duration,
			}}, "client": Clients.web    }))},url='https://shadmessenger78.iranlms.ir/').text)['data_enc']))
		except: pass

	def getChannelMembers(self, channel_guid, text=None, start_id=None):
		try:
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": Clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"channel_guid": channel_guid,
					"search_text": text,
					"start_id": start_id
				})),
				"method":"getChannelAllMembers"
			},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def getChannelLink(self, channel_guid,):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getChannelLink",
				"input":{
					"channel_guid": channel_guid
				},
				"client": Clients.web    }))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def finishVoiceChat(self, chat_id, voice_chat_id, on="Group"):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":f"discard{on}VoiceChat",
			"input":{
				f"{on.lower()}_guid":chat_id,
				"voice_chat_id" : voice_chat_id,
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def getAvatars(self,myguid):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getAvatars",
			"input":{
				"object_guid":myguid,
			},
			"client": Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc"))).get("data").get("avatars")

	def setChannelLink(self, channel_guid,):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setChannelLink",
			"input":{
				"channel_guid": channel_guid
			},
			"client":Clients.web
		}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))

	def searchGlobalObjects(self, search_text):
		try:
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": Clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"search_text": search_text
				})),
				"method": "searchGlobalObjects"
			}, url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def addGroupMembers(self, group_guid, user_ids):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"addGroupMembers",
				"input":{
					"group_guid": group_guid,
					"member_guids": user_ids
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json()["data_enc"]))
		except: pass

	def getInfoByUsername(self, username,):
		try:
			if '@' in username: username = username.replace('@', '')
			else: username = username
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getObjectByUsername",
				"input":{
					"username": username
				},
				"client": Clients.web
			}))},url='https://shadmessenger78.iranlms.ir/').json().get("data_enc")))
		except: pass

class Uploader:
	def __init__(self, auth,):
		self.auth=Bot(auth)

	def sendPhoto(self,object_guid, file, caption=None, message_id=None,):
		if caption!=None and message_id!=None:
			byte=open(file, 'rb').read()
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile('TyperGames.png', len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, 'TyperGames.png', len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,text=caption, message_id=message_id)
		elif caption==None and message_id==None:
			byte=open(file, 'rb').read()
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile('TyperGames.png', len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, 'TyperGames.png', len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,)
		elif message_id!=None:
			byte=open(file, 'rb').read()
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile('TyperGames.png', len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, 'TyperGames.png', len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,message_id=message_id,)
		elif caption!=None:
			byte=open(file, 'rb').read()
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile('TyperGames.png', len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, 'TyperGames.png', len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,text=caption,)

	def sendPhotoWithLink(self, object_guid, link, caption=None, message_id=None):
		file_name='TyperGames'+str(randint(10000, 999999999))+'.png'
		if caption!=None and message_id!=None:
			byte=get(str(link)).content
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile(file_name, len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, file_name, len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,text=caption, message_id=message_id)
		elif (caption==None and message_id==None):
			byte=get(str(link)).content
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile(file_name, len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, file_name, len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,)
		elif caption!=None:
			byte=get(str(link)).content
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile(file_name, len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, file_name, len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height,text=caption,)
		elif message_id!=None:
			byte=get(str(link)).content
			[width,height]=self.auth.getImageSize(byte)
			rsf=self.auth.requestSendFile(file_name, len(byte), 'png') # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendImage(object_guid ,rsf['id'] , 'png', rsf['dc_id'] , access, file_name, len(byte), str(self.auth.getThumbInline(byte))[2:-1] , width, height, message_id=message_id,)

	def sendDocument(self, object_guid, file, file_name=None,caption=None, message_id=None):
		suffix = Path(file).suffix
		if file_name==None:
			file_name='TyperGames'+str(randint(10000, 999999999))+suffix
		else:
			file_name=file_name+suffix
		if caption!=None and message_id!=None:
			byte=open(file, 'rb').read()
			rsf=self.auth.requestSendFile(file_name, len(byte), suffix[1:]) # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendFile(object_guid,rsf['id'] , suffix[1:], rsf['dc_id'] , access, file_name, len(byte), text=caption,message_id=message_id,)
		elif caption==None and message_id==None:
			byte=open(file, 'rb').read()
			rsf=self.auth.requestSendFile(file_name, len(byte), suffix[1:]) # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendFile(object_guid,rsf['id'] , suffix[1:], rsf['dc_id'] , access, file_name, len(byte),)
		elif message_id!=None:
			byte=open(file, 'rb').read()
			rsf=self.auth.requestSendFile(file_name, len(byte), suffix[1:]) # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendFile(object_guid,rsf['id'] , suffix[1:], rsf['dc_id'] , access, file_name, len(byte), message_id=message_id)
		elif caption!=None:
			byte=open(file, 'rb').read()
			rsf=self.auth.requestSendFile(file_name, len(byte), suffix[1:]) # rsf = request send File
			if rsf!='many_request':
				access = self.auth.fileUpload(byte, rsf['access_hash_send'], rsf['id'], rsf['upload_url'])
				self.auth.sendFile(object_guid,rsf['id'] , suffix[1:], rsf['dc_id'] , access, file_name, len(byte), text=caption)