# WhatsApp Bulk Messages Without Saving Contacts

This Python script sends WhatsApp messages automatically via WhatsApp Web without requiring saved contacts. It can be configured to send promotional or informational messages to recipients. Originally designed to read data from an Excel sheet, it can be adapted to read phone numbers and messages from other sources.

## Important Note

As of May 2022, WhatsApp Business offers official APIs, rendering this workaround less necessary. You may consider using WhatsApp Business APIs for a more stable and officially supported solution.

## Prerequisites

- **Python 3.8 or later**: [Download](https://www.python.org/downloads/)
- **Google Chrome (v79 or later)**: [Download](https://www.google.com/chrome/)
- **pipenv**: Run `pip install --user pipenv`
  
After installing `pipenv`, navigate to the project directory and run:

```bash
pipenv shell
pipenv install selenium webdriver-manager
```

This ensures all dependencies are managed within a virtual environment.

## Approach

1. Clone this repository.
2. Ensure `data.txt` and `text.txt` or relevant input files are placed in the project directory.
3. Run the script:

   ```bash
   python script.py
   ```

4. A Chrome window will open with WhatsApp Web loaded. Scan the QR code using your phone.
5. Once the chat interface is visible, follow the terminal instructions.
6. The script will send messages to each contact and close automatically when finished.

## Sending Media

To send images or other media files, modify the code to include attachment handling. Note that sending attachments might require adjustments to element selection and waiting times.

## Legal

This code is not affiliated with, authorized, maintained, sponsored, or endorsed by WhatsApp or any of its affiliates. Use it at your own risk. Commercial use of this code is strictly prohibited.

---

**Note**: If the WhatsApp Web interface changes, the script may require updates to its selectors (such as XPath). If you encounter issues, feel free to reach out for assistance.
