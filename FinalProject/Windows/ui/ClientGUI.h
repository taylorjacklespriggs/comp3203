#ifndef CLIENTGUI_H
#define CLIENTGUI_H

#include <unordered_map>

#include <gtkmm/window.h>
#include <gtkmm/button.h>
#include <gtkmm/grid.h>
#include <gtkmm/frame.h>

#include "../DigiBoxClient.h"

class ClientGUI : public Gtk::Window {
    public:
        ClientGUI(DigiBoxClient *c);
        ~ClientGUI();

    private:
        DigiBoxClient *client;
        Gtk::Grid mainLayout;
        Gtk::Button fileButton;
        Gtk::Frame metaFrame;
        Gtk::Grid *metaLayout;
        Gtk::Button queueButton;
        Gtk::Button playButton;
        Gtk::Button pauseButton;
        Gtk::Button nextButton;
        void changeMetaFrame(std::string filePath, std::unordered_map<std::string, std::string> metadata);
        void clearMetaFrame();
        void on_fileButton_clicked();
        void on_queueButton_clicked();
        void on_playButton_clicked();
        void on_pauseButton_clicked();
        void on_nextButton_clicked();
        void streamState();
        static void streamStateWrap(ClientGUI *me);
        void setMargins(Gtk::Widget *w, int to, int ri, int bo, int le);

};

#endif
