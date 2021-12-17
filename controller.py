from model import Menu

main_menu = Menu(title="Menu principal: ",
                 add_info="(Tapez le chiffre correspondant à votre choix)",
                 item=["Gestion des joueurs",
                       "Gestion des tournois",
                       "Quitter"])


main_menu.display_menu()