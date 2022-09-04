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

    myKey = privateKey('0a7467a387acfbfac6c1697bcd5adf303eb290fc26da7ec08851b346cb8a9daa')
    myWalletAddress = publicKey(myKey)

    p1key = privateKey('b8f1923e48341ef53bd43b0a5b0eec544f2b4d968f9b193a92fc1c4a16656289')
    p1Wallet = publicKey(p1key)

    p2key = privateKey('e4ded3b4170609dace2d8e5e6c2af8d4a412a5f98672a2cc1de64ad7eec089fa')
    p2Wallet = publicKey(p2key)

    send(myWalletAddress, p2Wallet, 10, myKey)
    mining(myWalletAddress)
    getBalance(myWalletAddress)
    print('------')
    send(p1Wallet, myWalletAddress, 200, p1key)
    send(p2Wallet, myWalletAddress, 10, p2key)
    send(myWalletAddress, p1Wallet, 10, myKey)

    getBalance(myWalletAddress)
    mining(myWalletAddress)
    getBalance(myWalletAddress)


    Coin.chain[1].transaction[0].amount = 5000               #Test 

    print('Is chain valid?', Coin.isChainValid())           #Check valid of chain
    
    send(myWalletAddress, p2Wallet, 10, myKey)
    mining(myWalletAddress)
    getBalance(myWalletAddress)
    
    Coin.printChain()         #Show all block

if __name__ == '__main__':
    main()
    
