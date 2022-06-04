const ethers = require('ethers');
const fs = require('fs-extra');
require('dotenv').config();

async function main() {
    const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
    const encryptedJson = fs.readFileSync("./.encryptKey.json", "utf-8");
    // let wallet = new ethers.Wallet.fromEncryptedJsonSync(encryptedJson, process.env.PRIVATE_KEY_PASSWORD)
    // wallet = await wallet.connect(provider);
    const abi = fs.readFileSync('./SimpleStorage_sol_SimpleStorage.abi', 'utf-8');
    const bin = fs.readFileSync('./SimpleStorage_sol_SimpleStorage.bin', 'utf-8');

    const contractFactory = new ethers.ContractFactory(abi, bin, wallet);
    console.log('Deploying, please wait .......');

    const contract = await contractFactory.deploy();
    const deploymentReceipt = await contract.deployTransaction.wait(1);
    console.log(contract.address)

    const transactionResponse = await contract.store(7);
    const transactionReceipt = await transactionResponse.wait(1);
    const currentFavoriteNumber = await contract.retrieve();
}

main();