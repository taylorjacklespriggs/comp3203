#include <thread>
#include <iostream>
#include <gtkmm/label.h>
#include <gtkmm/separator.h>
#include <gtkmm.h>
#include <pangomm/fontdescription.h>
#include <gtkmm/cssprovider.h>
#include <gtkmm/stylecontext.h>
#include "ClientGUI.h"

ClientGUI::ClientGUI(DigiBoxClient *c) :
    client(c),
    fileButton("Choose Song"),
    metaFrame("Selected Song"),
    queueButton("Stream Song"),
    pauseButton("Pause/Play"), 
    nextButton("Next")
{
    // Extra form elements
    Gtk::Label *title = Gtk::manage(new Gtk::Label("DigiBox"));
    Gtk::Label *strmLabel = Gtk::manage(new Gtk::Label("Add a song to the playlist"));
    metaLayout = Gtk::manage(new Gtk::Grid());
    Gtk::Label *label = Gtk::manage(new Gtk::Label("Please select a song."));
    Gtk::Separator *partition = Gtk::manage(new Gtk::Separator());
    Gtk::Label *ctrlLabel = Gtk::manage(new Gtk::Label("Playback controls"));

    // Load CSS style
    auto css = Gtk::CssProvider::create();
    css->load_from_path("style.css");
    get_style_context()->add_provider_for_screen(get_screen(), css, GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);

    // Add CSS classes
    title->get_style_context()->add_class("title");
    strmLabel->get_style_context()->add_class("heading");
    ctrlLabel->get_style_context()->add_class("heading");

    // Set styling options
    fileButton.set_relief(Gtk::RELIEF_NONE);
    queueButton.set_relief(Gtk::RELIEF_NONE);
    pauseButton.set_relief(Gtk::RELIEF_NONE);
    nextButton.set_relief(Gtk::RELIEF_NONE);

    set_default_size(400, 400);

    fileButton.set_hexpand(true);
    metaFrame.set_vexpand(true);
    label->set_hexpand(true);
    label->set_vexpand(true);

    strmLabel->set_halign(Gtk::ALIGN_START);
    ctrlLabel->set_halign(Gtk::ALIGN_START);

    queueButton.set_sensitive(false);

    setMargins(&fileButton,10,10,10,10);
    setMargins(strmLabel,10,10,0,10);
    setMargins(&metaFrame,0,10,0,10);
    setMargins(&queueButton,10,10,10,10);
    setMargins(partition,0,10,0,10);
    setMargins(ctrlLabel,10,10,0,10);
    setMargins(&pauseButton,10,5,10,10);
    setMargins(&nextButton,10,10,10,5);

    // Attach elements to grids
    metaLayout->attach(*label, 0, 0, 1, 1);
    metaFrame.add(*metaLayout);

    mainLayout.attach(*title, 0, 0, 2, 1);
    mainLayout.attach(*strmLabel, 0, 1, 2, 1);
    mainLayout.attach(fileButton, 0, 2, 2, 1);
    mainLayout.attach(metaFrame, 0, 3, 2, 1);
    mainLayout.attach(queueButton, 0, 4, 2, 1);
    mainLayout.attach(*partition, 0, 5, 2, 1);
    mainLayout.attach(*ctrlLabel, 0, 6, 2, 1);
    mainLayout.attach(pauseButton, 0, 7, 1, 1);
    mainLayout.attach(nextButton, 1, 7, 1, 1);

    // Display elements
    add(mainLayout);
    show_all_children();

    // Connect button handlers
    fileButton.signal_clicked().connect(sigc::mem_fun(*this,
              &ClientGUI::on_fileButton_clicked));
    queueButton.signal_clicked().connect(sigc::mem_fun(*this,
              &ClientGUI::on_queueButton_clicked));
    pauseButton.signal_clicked().connect(sigc::mem_fun(*this,
              &ClientGUI::on_pauseButton_clicked));
    nextButton.signal_clicked().connect(sigc::mem_fun(*this,
              &ClientGUI::on_nextButton_clicked));
}

ClientGUI::~ClientGUI() {
}

void ClientGUI::changeMetaFrame(std::string filePath, std::unordered_map<std::string, std::string> metadata) {
    clearMetaFrame();

    // show file path
    metaLayout = Gtk::manage(new Gtk::Grid());
    Gtk::Label *pathKey = Gtk::manage(new Gtk::Label("Path:    "));
    pathKey->set_halign(Gtk::ALIGN_END);
    Gtk::Label *pathVal = Gtk::manage(new Gtk::Label(filePath));
    pathVal->set_halign(Gtk::ALIGN_START);
    pathVal->set_hexpand(true);
    metaLayout->attach(*pathKey, 0, 0, 1, 1);
    metaLayout->attach(*pathVal, 1, 0, 1, 1);

    // show rest of metadata
    int i=0;
    for (auto it = metadata.begin(); it != metadata.end(); ++it) {
        std::string key = it->first + ":    ";
        key[0] = toupper(key[0]);
        std::string val = it->second;
        val[0] = toupper(val[0]);
        Gtk::Label *keyLbl = Gtk::manage(new Gtk::Label(key));
        keyLbl->set_halign(Gtk::ALIGN_END);
        Gtk::Label *valLbl = Gtk::manage(new Gtk::Label(val));
        valLbl->set_halign(Gtk::ALIGN_START);
        metaLayout->attach(*keyLbl, 0, ++i, 1, 1);
        metaLayout->attach(*valLbl, 1, i, 1, 1);
    }
    metaFrame.add(*metaLayout);
    metaFrame.set_label("Selected Song");
    queueButton.set_sensitive(true);
    show_all_children();
}

void ClientGUI::clearMetaFrame() {
    std::vector<Gtk::Widget *> widgets = metaFrame.get_children();
    for (int i = 0; i < widgets.size(); i++) {
        metaFrame.remove();
        delete(widgets[i]);
    }
}

void ClientGUI::on_fileButton_clicked() {
  Gtk::FileChooserDialog dialog("Please choose a file",
          Gtk::FILE_CHOOSER_ACTION_OPEN);
  dialog.set_transient_for(*this);

  dialog.reset_style();

  //Add response buttons the the dialog:
  dialog.add_button("_Cancel", Gtk::RESPONSE_CANCEL);
  dialog.add_button("_Open", Gtk::RESPONSE_OK);

  //Add filters, so that only certain file types can be selected:
  
  auto filter_mp3 = Gtk::FileFilter::create();
  filter_mp3->set_name("Audio files");
  filter_mp3->add_pattern("*.mp3");
  filter_mp3->add_pattern("*.wav");
  filter_mp3->add_pattern("*.ogg");
  filter_mp3->add_pattern("*.acc");
  filter_mp3->add_pattern("*.ogg");
  filter_mp3->add_pattern("*.m4a");
  filter_mp3->add_pattern("*.mov");
  filter_mp3->add_pattern("*.avi");
  filter_mp3->add_pattern("*.mp4");
  filter_mp3->add_pattern("*.mkv");
  dialog.add_filter(filter_mp3);

  //Show the dialog and wait for a user response:
  int result = dialog.run();

  //Handle the response:
  switch(result)
  {
    case(Gtk::RESPONSE_OK):
    {
      std::cout << "Open clicked." << std::endl;

      //Notice that this is a std::string, not a Glib::ustring.
      std::string filename = dialog.get_filename();
      std::cout << "File selected: " <<  filename << std::endl;
      changeMetaFrame(filename, client->setMetadata(filename));
      break;
    }
    case(Gtk::RESPONSE_CANCEL):
    {
      std::cout << "Cancel clicked." << std::endl;
      break;
    }
    default:
    {
      std::cout << "Unexpected button clicked." << std::endl;
      break;
    }
  }
}

void ClientGUI::streamState() {
    fileButton.set_sensitive(false);
    queueButton.set_sensitive(false);
    client->connect();
    fileButton.set_sensitive(true);
    queueButton.set_sensitive(true);
}

void ClientGUI::streamStateWrap(ClientGUI *me) {
    me->streamState();
}

void ClientGUI::on_queueButton_clicked() {
    std::thread streamThread(&ClientGUI::streamStateWrap, this);
    streamThread.detach();
}

void ClientGUI::on_pauseButton_clicked() {
    std::thread t(&ClientGUI::playbackWrap, this, "pause");
    t.detach();
}

void ClientGUI::on_nextButton_clicked() {
    std::thread t(&ClientGUI::playbackWrap, this, "next");
    t.detach();
}

void ClientGUI::playbackWrap(ClientGUI *me, std::string action) {
    me->client->playbackAction(action);
}

void ClientGUI::setMargins(Gtk::Widget *w, int to, int ri, int bo, int le) {
    w->set_margin_top(to);
    w->set_margin_right(ri);
    w->set_margin_bottom(bo);
    w->set_margin_left(le);
}
