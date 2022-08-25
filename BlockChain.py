from asyncio.windows_events import NULL
from datetime import datetime
from hashlib import sha256
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1, keys

class Transaction:
    def __init__(self, fromAdd, toAdd, amount):
        self.fromAdd = fromAdd
        self.toAdd = toAdd
        self.amount = amount

    def calHash(self):
        if type(self.toAdd) == str:
            return sha256(str(self.fromAdd.to_string().hex() + self.toAdd + str(self.amount)).encode('utf-8')).hexdigest()
        return sha256(str(self.fromAdd.to_string().hex() + self.toAdd.to_string().hex() + str(self.amount)).encode('utf-8')).hexdigest()

    def signTrans(self, sk):
        if (sk.verifying_key != self.fromAdd):
            raise ValueError('You can\'t sign transaction for other wallet!')

        hashTrans = self.calHash()
        sig = SigningKey.sign(sk,hashTrans.encode('utf-8'))
        self.signature = sig

    def isValid(self):
        if(self.fromAdd == NULL): return True
        if(not self.signature or len(self.signature) == 0):
            raise ValueError('No signature in this transaction')

        pubkey = VerifyingKey.from_string(self.fromAdd.to_string(), SECP256k1)
        try:
            return pubkey.verify(self.signature, self.calHash().encode())
        except: 
            return False

class Block:
    fm = '%d/%m/%Y'
    def __init__(self, timestamp, transaction:Transaction, previousHash = ""):
        self.timestamp = timestamp.strftime(Block.fm)
        # self.ty = type(transaction)
        # if (self.ty == dict):
        #     for k,v in transaction.items():
        #         self.key = k
        #         self.val = v
        #     self.transaction = k+':'+str(v)
        # else: 
        #     self.transaction = transaction
        self.transaction = transaction
        self.previousHash = previousHash
        self.nonce = int(0)
        self.hash = self.calHash()

        # self.fromAdd = 
        # self.toAdd = 
        # self.amount = 
        

    def calHash(self):
        # ty = type(self.transaction)
        # if (ty == dict):
        #     for k,v in self.transaction.items():
        #         self.key = k
        #         self.val = v
        #     self.transaction = k+':'+str(v)
        return sha256(str(self.previousHash + self.timestamp + str(self.nonce)).encode('utf-8')).hexdigest()

    def __str__(self) -> dict:
        # if (self.ty == dict):
        #     return {
        #         'index' : self.index,
        #         'timestamp' : self.timestamp,
        #         self.key : self.val,
        #         'previousHash' : self.previousHash,
        #         'hash' : self.hash
        #     }
        # else:
        # trans = self.transaction
        # fa = trans.fromAdd
        # ta = trans.toAdd
        return {
            'timestamp' : self.timestamp,
            # "fromAddress" : self.fromAdd,
            # "toAddress" : self.toAdd,
            # "amount" : self.amount,
            'previousHash' : self.previousHash,
            'hash' : self.hash
        }

    def mineBlock(self, difficulty):

        while(self.hash[:difficulty] != ''.join(['0' for i in range(difficulty)])):
            self.nonce += 1
            self.hash = self.calHash()

        print("Block mined: " + self.hash)

    def hasValidTrans(self):
        trans = self.transaction
        for tran in trans:
            if (not tran.isValid()):
                return False

        return True
class BlockChain:
    def __init__(self):
        self.chain = [self.genesisBlock()]
        self.difficulty = 3
        self.pendingTrans = []
        self.miningReward = 100

    def genesisBlock(self):
        return Block(datetime(2022, 8, 1),"GenesisBlock","0")

    def getLastesBlock(self):
        return self.chain[len(self.chain)-1]

    def minePendingTrans(self, miningRewardAdd):
        rewardTx = Transaction(NULL, miningRewardAdd, self.miningReward)
        self.pendingTrans.append(rewardTx)

        block = Block(datetime.now(), self.pendingTrans,self.getLastesBlock().hash)
        block.mineBlock(self.difficulty)

        print('Block successfully mined!')
        self.chain.append(block)

        self.pendingTrans = []

    def addTrans(self,trans):

        if (not trans.fromAdd or not trans.toAdd):
            raise ValueError('Transaction must include from and to address')

        if (not trans.isValid()):
            raise ValueError('Cant\' add invalid transction to chain')

        self.pendingTrans.append(trans)

    def getBalance(self, address):
        balance = 0
        
        for block in self.chain:
            trans = block.transaction
            if trans == 'GenesisBlock': continue
            for add in trans:
                if add.fromAdd == address:
                    balance -= add.amount
                if add.toAdd == address:
                    balance += add.amount

        return balance

    def printChain(self):
        for i in range(len(self.chain)):
            # if i == 0: continue
            print(json.dumps(self.chain[i].__str__(),separators=('',':'),indent=2))

    def isChainValid(self):
        for i in range(len(self.chain)):
            if i == 0: continue
            CurBlock = self.chain[i]
            PreBlock = self.chain[i-1]
            
            if not CurBlock.hasValidTrans(): return False

            if CurBlock.hash != CurBlock.calHash(): return False
            
            if CurBlock.previousHash != PreBlock.hash: return False

        return True
