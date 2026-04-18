import main_window

RELOAD=1

if RELOAD:
    try:
        from importlib import reload
        load_ui=reload(main_window)
    except:
        load_ui=reload(main_window)

    # try: 
    #     AbinTools_UI.show()
    #     AbinTools_UI.raise_()
    # except:

    try:
        AbinTools_UI.close()
        AbinTools_UI.deleteLater()
    except:
        pass

    AbinTools_UI=load_ui.MainFLWin()
    AbinTools_UI.show()
else:
    main_window.Show()
