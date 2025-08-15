# bot_gui_generator_complet.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def generate_bot_script(token, log_channel_id, include_wallpaper, include_screenshot, include_run):
    lines = [
        "import discord",
        "from discord.ext import commands",
        "import pyautogui",
        "import ctypes",
        "import os",
        f"TOKEN = '{token}'",
        f"LOG_CHANNEL_ID = {log_channel_id}",
        "PREFIX = '!'",
        "",
        "# --- Intents nécessaires ---",
        "intents = discord.Intents.default()",
        "intents.message_content = True",
        "intents.guilds = True",
        "intents.messages = True",
        "",
        "bot = commands.Bot(command_prefix=PREFIX, intents=intents)",
        ""
    ]

    if include_wallpaper:
        lines += [
            "@bot.command()",
            "async def wallpaper(ctx, path: str):",
            "    if os.path.exists(path):",
            "        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)",
            "        await ctx.send(f'Fond d\\'écran changé : {path}')",
            "        log_channel = bot.get_channel(LOG_CHANNEL_ID)",
            "        if log_channel: await log_channel.send(f'[LOG] Fond d\\'écran changé : {path}')",
            "    else:",
            "        await ctx.send('Le fichier n\\'existe pas.')",
            ""
        ]

    if include_screenshot:
        lines += [
            "@bot.command()",
            "async def screenshot(ctx):",
            "    screenshot = pyautogui.screenshot()",
            "    save_path = 'screenshot.png'",
            "    screenshot.save(save_path)",
            "    await ctx.send(file=discord.File(save_path))",
            "    log_channel = bot.get_channel(LOG_CHANNEL_ID)",
            "    if log_channel: await log_channel.send('[LOG] Capture d\\'écran envoyée')",
            ""
        ]

    if include_run:
        lines += [
            "@bot.command()",
            "async def run(ctx, program: str):",
            "    try:",
            "        os.startfile(program)",
            "        await ctx.send(f'{program} lancé !')",
            "        log_channel = bot.get_channel(LOG_CHANNEL_ID)",
            "        if log_channel: await log_channel.send(f'[LOG] Programme lancé : {program}')",
            "    except Exception as e:",
            "        await ctx.send(f'Erreur : {e}')",
            ""
        ]

    lines += ["print('Connexion au bot…')", "bot.run(TOKEN)"]
    return "\n".join(lines)

# --- GUI ---
def generate_script_gui():
    token = entry_token.get()
    log_channel = entry_log_channel.get()
    include_wallpaper = var_wallpaper.get()
    include_screenshot = var_screenshot.get()
    include_run = var_run.get()

    if not token or not log_channel:
        messagebox.showerror("Erreur", "Vous devez entrer le token et l'ID du salon de log !")
        return

    try:
        log_channel_id = int(log_channel)
    except:
        messagebox.showerror("Erreur", "L'ID du salon doit être un nombre entier.")
        return

    script = generate_bot_script(token, log_channel_id, include_wallpaper, include_screenshot, include_run)
    save_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(script)
        messagebox.showinfo("Succès", f"Script généré à {save_path}")

root = tk.Tk()
root.title("Bot Discord Script Generator Complet")

tk.Label(root, text="Token du bot Discord:").pack()
entry_token = tk.Entry(root, width=50)
entry_token.pack()

tk.Label(root, text="ID du salon Discord pour les logs:").pack()
entry_log_channel = tk.Entry(root, width=50)
entry_log_channel.pack()

var_wallpaper = tk.IntVar()
var_screenshot = tk.IntVar()
var_run = tk.IntVar()

tk.Checkbutton(root, text="Inclure commande changement fond d'écran", variable=var_wallpaper).pack()
tk.Checkbutton(root, text="Inclure commande capture écran", variable=var_screenshot).pack()
tk.Checkbutton(root, text="Inclure commande lancer programme", variable=var_run).pack()

tk.Button(root, text="Générer le script .py", command=generate_script_gui).pack(pady=10)

root.mainloop()
