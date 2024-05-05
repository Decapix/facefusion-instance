import subprocess

def run_command():
    # Définition de la commande
    command = [
        "python", "run.py",
        "--headless",
        "--source", "exec/base.png",
        "--target", "exec/vid2.mp4",
        "--output", "exec/result/vid2-res.mp4"
    ]

    # Exécution de la commande
    try:
        subprocess.run(command, check=True)
        print("La commande a été exécutée avec succès.")
    except subprocess.CalledProcessError as e:
        print("Une erreur s'est produite lors de l'exécution de la commande.")
        print(e)

if __name__ == "__main__":
    run_command()
