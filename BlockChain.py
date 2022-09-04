from asyncio.windows_events import NULL
from datetime import datetime
from hashlib import sha256
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1, keys

class Transaction:
    '''
    Make a Transaction
    '''
    def __init__(self, fromAdd, toAdd : VerifyingKey, amount):
        self.fromAdd = fromAdd
        self.toAdd = toAdd
        self.amount = amount

    def calHash(self):
        '''
        Make hash for signature
        Hash make up of FromAddress, ToAddress, Amount
        '''
        if type(self.toAdd) == str:
            return sha256(str(self.fromAdd.to_string().hex() + self.toAdd + str(self.amount)).encode('utf-8')).hexdigest()
        return sha256(str(self.fromAdd.to_string().hex() + self.toAdd.to_string().hex() + str(self.amount)).encode('utf-8')).hexdigest()

    def signTrans(self, sk):
        '''
        Sign the Transaction to authenticate the owner of the wallet/sender
        '''
        if (sk.verifying_key != self.fromAdd):          #Verify owner/sender PublicKey
            raise ValueError('You can\'t sign transaction for other wallet!')

        hashTrans = self.calHash()          # Make hash for signing
        sig = SigningKey.sign(sk,hashTrans.encode('utf-8'))     #Signing Transaction
        self.signature = sig

    def isValid(self):
        '''
        Validate Transaction
        '''
        if(self.fromAdd == NULL): return True           #Validate for the mining reward
        if(not self.signature or len(self.signature) == 0):         #Check for Signature
            raise ValueError('No signature in this transaction')

        pubkey = VerifyingKey.from_string(self.fromAdd.to_string(), SECP256k1)  #Extract PublicKey
        try:
            return pubkey.verify(self.signature, self.calHash().encode())       #Verifying signature
        except: 
            return False

class Block:
    fm = '%d/%m/%Y'
    def __init__(self, timestamp, transaction:Transaction, previousHash = ""):
        '''
        Make a block
        '''
        self.timestamp = timestamp.strftime(Block.fm)
        self.transaction = transaction
        self.previousHash = previousHash
        self.nonce = int(0)
        self.toAdress = []
        self.fromAdress = []
        self.amount = []
        trans = self.transaction
        if trans != 'GenesisBlock':
            for i in trans:
                self.toAdress.append(i.toAdd.to_string().hex())
                if type(i.fromAdd) != int:
                    self.fromAdress.append(i.fromAdd.to_string().hex())
                self.amount.append(str(i.amount))
        self.hash = self.calHash()
      
    def calHash(self):
        '''
        Make block's hash
        '''
        return sha256((self.previousHash + self.timestamp + str(self.nonce) + ', '.join(self.fromAdress) + ', '.join(self.toAdress) + ', '.join(self.amount)).encode()).hexdigest()

    def __str__(self) -> dict:
        '''
        print Block
        '''
        return {
            'timestamp' : self.timestamp,
            'previousHash' : self.previousHash,
            'hash' : self.hash,
            'nonce': self.nonce,
            'FromAddress' : ', '.join(self.fromAdress),
            'ToAddress' : ', '.join(self.toAdress),
            'Amount' : ', '.join(self.amount)
        }

    def mineBlock(self, difficulty):
        '''
        mine Block with a difficulty
            ex: difficulty = 3 -> block's hash: 000+hash
        '''

        while(self.hash[:difficulty] != \
            ''.join(['0' for i in range(difficulty)])):
            self.nonce += 1
            self.hash = self.calHash()

        print("Block mined: " + self.hash)

    def hasValidTrans(self):
        '''
        Confirm the transaction
        '''
        trans = self.transaction
        for tran in trans:
            if (not tran.isValid()):
                return False

        return True

class BlockChain:
    '''
    Make a Chain of Block with difficulty of hash
    '''
    def __init__(self, difficulty):
        self.chain = [self.genesisBlock()]      # Make a Chain with the first block is Genesis Block
        self.difficulty = difficulty                     
        self.pendingTrans = []                  # Make a list of pending transaction
        self.miningReward = 100

    def genesisBlock(self):
        '''
        make The First Block: The Beginning of the Chain
        '''
        return Block(datetime(2022, 8, 1),"GenesisBlock","0")

    def getLastBlock(self):
        '''
        get The Last Block: The End of the Chain
        '''
        return self.chain[len(self.chain)-1]

    def minePendingTrans(self, miningRewardAdd):
        '''
        add a mined Block to a pending chain for a pending Transaction
        '''
        rewardTx = Transaction(NULL, miningRewardAdd, self.miningReward)    #This transaction will send reward to the miner
        self.pendingTrans.append(rewardTx)                                  #Send this transaction to pending chain

        block = Block(datetime.now(), self.pendingTrans,self.getLastBlock().hash)     # Make a block consist of the made time, list of pending Trans and the last block's hash
        block.mineBlock(self.difficulty)

        print('Block successfully mined!')
        self.chain.append(block)            # Add Block to Chain

        self.pendingTrans = []              # Empty pending List

    def addTrans(self,trans):
        '''
        Add Transaction to pending list wait for a block
        '''

        if (not trans.fromAdd or not trans.toAdd):              # Check for address
            raise ValueError('Transaction must include from and to address')

        if (not trans.isValid()):                               # Check for Signature
            raise ValueError('Cant\' add invalid transction to chain')

        self.pendingTrans.append(trans)                         # Add transaction to a pending list

    def getBalance(self, address):
        '''
        Get Balance of a Address
        Because there is no saved file or database, we get balance by calculating how many Coins get in and out of the address
        '''

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
        '''
        Show all the block
        '''
        for i in range(len(self.chain)):
            if i == 0: continue
            print(json.dumps(self.chain[i].__str__(),separators=('',':'),indent=2))

    def isChainValid(self):
        '''
        Check the Chain if:
            There is invalid Transaction
            There is Wrong Hash of the current Block
            There is Wrong Hash of the previous Block
        '''
        for i in range(len(self.chain)):
            if i == 0: continue
            CurBlock = self.chain[i]
            PreBlock = self.chain[i-1]
            
            if not CurBlock.hasValidTrans(): return False

            if CurBlock.hash != CurBlock.calHash(): return False
            
            if CurBlock.previousHash != PreBlock.hash: return False

        return True
