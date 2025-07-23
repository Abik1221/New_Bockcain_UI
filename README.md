# MemeCoin Generator

Welcome to the MemeCoin Generator, a desktop application built with Python that allows you to deploy and manage custom ERC-20 tokens on the Ethereum Sepolia testnet. This project features a pygame-based UI, making it both functional and interactive.

---

## Prerequisites

- Python 3.x installed on your system
- A stable internet connection (for Infura and test ETH faucets)
- MetaMask browser extension for wallet management

---

## Getting Started

Follow these steps to set up and run the MemeCoin Generator on your local machine.

### 1. Clone or Download the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/your-username/meme-coin-generator.git
```

(Replace the URL with your repository link if hosted, or download the ZIP file and extract it.)

Navigate to the project folder:

```sh
cd meme-coin-generator
```

### 2. Create a Virtual Environment

A virtual environment helps isolate project dependencies. Create and activate it with the following commands:

**Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```sh
python3 -m venv venv
source venv/bin/activate
```

Once activated, you should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```sh
pip install -r requirements.txt
```

If `requirements.txt` is not present, create it with the following content and run the command again:

```
pygame==2.5.2
web3==6.0.0
py-solc-x==1.1.2
python-dotenv==1.0.0
pyinstaller==5.13.2
pyperclip==1.9.0
```

> **Note:** Your current `requirements.txt` may be corrupted or incomplete. Ensure it contains the above packages for full functionality.

### 4. Configure the `.env` File

The `.env` file stores sensitive configuration data. Create it in the project root and add your own details:

Create the `.env` file:

```sh
touch .env
```

Open `.env` in a text editor and add the following, replacing the placeholders with your own values:

```
PRIVATE_KEY=your_metamask_private_key
WALLET_ADDRESS=your_public_wallet_address
INFURA_URL=https://sepolia.infura.io/v3/your_infura_project_id
CHAIN_ID=11155111
```

- **PRIVATE_KEY:** A 64-character hexadecimal string. Export this from MetaMask by going to Account Details > Export Private Key after creating a wallet. (For security, never share this key publicly.)
- **WALLET_ADDRESS:** A 42-character Ethereum address (e.g., starting with 0x). Copy this from MetaMask’s public address field.
- **INFURA_URL:** Sign up at [infura.io](https://infura.io), create a new project for the Sepolia network, and use the format `https://sepolia.infura.io/v3/your_project_id` (replace `your_project_id` with your unique Infura Project ID).
- **CHAIN_ID:** Set to `11155111`, the chain ID for the Sepolia testnet.

**Fund Your Wallet:**

- Open MetaMask, switch to the Sepolia network, and copy your `WALLET_ADDRESS`.
- Visit [sepoliafaucet.com](https://sepoliafaucet.com) or [faucet.paradigm.xyz](https://faucet.paradigm.xyz), paste your address, and request 0.1–0.5 test ETH (free, with a short wait).

---

### 5. Run the Application

Launch the UI by running:

```sh
python meme_coin_gui.py
```

A window should open with input fields for token deployment.

---

### 6. Package into an Executable (Optional)

To create a standalone executable:

```sh
pyinstaller --onefile --add-data "MemeCoin.sol;." --add-data ".env;." --add-data "blockchain.py;." meme_coin_gui.py
```

Find the executable in the `dist` folder (e.g., `meme_coin_gui.exe` on Windows) and run it.

---

## Usage

- **Deploy a Token:** Enter a token name, symbol, and initial supply in the input fields, then click “LAUNCH MEME COIN.”
- **View Status:** Check the status and deployment log for results and contract details.

---

## Project Structure

```
New_Bockcain_UI/
│
├── MemeCoin.sol           # Smart contract source
├── blockchain.py          # Blockchain logic
├── meme_coin_gui.py       # UI and main application
├── .env                   # Configuration file (not committed)
├── requirements.txt       # Dependency list
├── README.md              # Project documentation
└── __pycache__/           # Python cache files (ignored)
```

---

## Troubleshooting

- **Insufficient Funds:** If deployment fails, ensure your wallet has test ETH. Request more from the faucet.
- **Module Not Found:** Verify all dependencies are installed via `pip install -r requirements.txt`.
- **Connection Issues:** Check `INFURA_URL` and your internet connection.
- **Executable Errors:** Re-run the `pyinstaller` command and ensure all files are included.

---

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests. For issues or suggestions, please open an issue on GitHub.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details (create a LICENSE file if not present).

---

## Acknowledgments

- Inspired by Connect Four-style UI concepts.
- Utilizes Infura for Ethereum node access and Sepolia testnet for deployment.