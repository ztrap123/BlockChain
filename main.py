from BlockChain import BlockChain, Transaction
from ecdsa import SigningKey, VerifyingKey, SECP256k1

def main():

    def mining(address):              
        '''
        Mining Block (Address to send reward)
        '''
        print('Starting the miner...')
        Coin.minePendingTrans(address)

    def getBalance(address):            
        '''
        Show balance of Address
        '''
        print('Balance:', Coin.getBalance(address))

    def send(frm, to, amount, key):    
        '''
        Send Coin (frm: from address, to: to address, amount: amount of coin, key: Private key to sign)
        '''
        trans = Transaction(frm, to, amount)
        trans.signTrans(key)
        Coin.addTrans(trans)

    def privateKey(key):
        '''
        Convert hexkey to bytes for computer
        return -> Private Key
        '''
        return SigningKey.from_string(bytes.fromhex(key),curve=SECP256k1)
    def publicKey(key):
        '''
        Make Public key from Private key
        return -> Public Key
        '''
        return key.verifying_key
    # myKey = SigningKey.from_string(bytes.fromhex('899cad35b4857b41b3e439d9b86d6e3654193859de9e19d5590ea85343f608ae'),curve=SECP256k1)
    # myWalletAddress = myKey.verifying_key

    Coin = BlockChain(4)             #Generate the chain

    myKey = privateKey('899cad35b4857b41b3e439d9b86d6e3654193859de9e19d5590ea85343f608ae')
    myWalletAddress = publicKey(myKey)

    p1key = privateKey('ed1b8435585667c3ee34807d3a9a3a3e074bf20f86a6aad82427daa2f3690805')
    p1Wallet = publicKey(p1key)

    p2key = privateKey('7fb4d4c835e9fe9a8a4105fc750649fcfb1c38e75d282d94becdf40a66ae77a9')
    p2Wallet = publicKey(p2key)

    send(myWalletAddress, p2key, 10, myKey)
    mining(myWalletAddress)
    getBalance(myWalletAddress)
    print('------')
    send(p1Wallet, myWalletAddress, 200, p1key)
    send(p2Wallet, myWalletAddress, 10, p2key)
    send(myWalletAddress, p1Wallet, 10, myKey)

    getBalance(myWalletAddress)
    mining(myWalletAddress)
    getBalance(myWalletAddress)


    # Coin.chain[1].transaction[0].amount = 5               #Test 

    print('Is chain valid?', Coin.isChainValid())           #Check valid of chain
    
    Coin.printChain()         #Show all block

if __name__ == '__main__':
    main()
    
