from eth_abi.packed import encode_abi_packed
from web3 import Web3


# Python implementation of https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/libraries/UniswapV2Library.sol#L17-L26
# We need "factory_address" and "init_code_hash" configuration to make it work in different environments (Uniswap, Sushiswap etc...)
class HashService:

    @staticmethod
    def for_uniswap():
        return HashService(
            factory_address='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
            init_code_hash='0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f',
        )
    
    @staticmethod
    def for_sushiswap():
        return HashService(
            factory_address='0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac',
            init_code_hash='0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303',
        )
        
    @staticmethod
    def for_sushiswap_polygon():
        return HashService(
            factory_address='0xc35DADB65012eC5796536bD9864eD8773aBc74C4',
            init_code_hash='0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303',
        )
        
    @staticmethod
    def for_sushiswap_fantom():
        return HashService(
            factory_address='0xc35DADB65012eC5796536bD9864eD8773aBc74C4',
            init_code_hash='0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303',
        )

    @staticmethod
    def for_sushiswap_avalanche():
        return HashService(
            factory_address='0xc35DADB65012eC5796536bD9864eD8773aBc74C4',
            init_code_hash='0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303',
        )
    
    @staticmethod
    def for_quickswap():
        return HashService(
            factory_address='0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32',
            init_code_hash='0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f',
        )
        
    @staticmethod
    def for_spookyswap():
        return HashService(
            factory_address='0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3',
            init_code_hash='0xcdf2deca40a0bd56de8e3ce5c7df6727e5b1bf2ac96f283fa9c4b3e6b42ea9d2',
        )
        
    @staticmethod
    def for_traderjoe():
        return HashService(
            factory_address='0x9Ad6C38BE94206cA50bb0d90783181662f0Cfa10',
            init_code_hash='0x0bbca9af0511ad1a1da383135cf3a8d2ac620e549ef9f6ae3a4c33c2fed0af91',
        )
               
    @staticmethod
    def for_pancake_swap():
        return HashService(
            factory_address='0xBCfCcbde45cE874adCB698cC183deBcF17952812',
            init_code_hash='0xd0d4c4cd0848c93cb4fd1f498d7013ee6bfb25783ea21593d5834f5d250ece66',
        )


    def __init__(self, factory_address: str, init_code_hash: str):
        self.init_code_hash = init_code_hash
        self.factory_address = factory_address

    def calculate_pair_adress(self, tokenA, tokenB):
        tokenA = Web3.toChecksumAddress(tokenA)
        tokenB = Web3.toChecksumAddress(tokenB)

        tokenA_hex = bytes.fromhex(tokenA[2:])
        tokenB_hex = bytes.fromhex(tokenB[2:])
        if tokenA_hex < tokenB_hex:
            token0 = tokenA
            token1 = tokenB
        else:
            token1 = tokenA
            token0 = tokenB

        b_salt = Web3.keccak(encode_abi_packed(['address', 'address'], [token0, token1]))

        pre = '0xff'
        b_pre = bytes.fromhex(pre[2:])
        b_address = bytes.fromhex(self.factory_address[2:])
        b_init_code = bytes.fromhex(self.init_code_hash[2:])
        b_result = Web3.keccak(
            encode_abi_packed(['bytes', 'bytes', 'bytes', 'bytes'], [b_pre, b_address, b_salt, b_init_code]))
        result_address = Web3.toChecksumAddress(b_result[12:].hex())
        return result_address, token0, token1
