from BlockChain import BlockChain, Transaction
from ecdsa import SigningKey, VerifyingKey, SECP256k1
def main():
    myKey = SigningKey.from_string(bytes.fromhex('899cad35b4857b41b3e439d9b86d6e3654193859de9e19d5590ea85343f608ae'),curve=SECP256k1)
    myWalletAddress = myKey.verifying_key

    Coin = BlockChain()

    trans1 = Transaction(myWalletAddress, 'Public key goes here', 10)
    trans1.signTrans(myKey)
    Coin.addTrans(trans1)

    print('Starting the miner...')
    Coin.minePendingTrans(myWalletAddress)

    print('Balance of Blabla is', Coin.getBalance(myWalletAddress))

    # Coin.chain[1].transaction[0].amount = 5
    print('Is chain valid?', Coin.isChainValid())
    
    
    # Coin.printChain()

if __name__ == '__main__':
    main()
    
