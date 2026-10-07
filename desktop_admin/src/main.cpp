#include <QApplication>
#include <QStyleFactory>
#include "LoginDialog.h"
#include "MainWindow.h"
#include "DatabaseManager.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    app.setStyle(QStyleFactory::create("Fusion"));

    // PostgreSQL real DB bilan ulanish
    DatabaseManager::instance().connectToPostgres("localhost", 5432, "parkly_db", "postgres", "postgres");

    // 1. Tizimga kirish oynasi (Image 3 dizayni asosida)
    LoginDialog loginDlg;
    if (loginDlg.exec() == QDialog::Accepted) {
        // 2. Muvaffaqiyatli kirgach, Asosiy Dashboard (Image 1 & 2 dizayni asosida) ochiladi
        MainWindow mainWindow;
        mainWindow.setAuthenticatedUser(
            loginDlg.getLoggedInUsername(),
            loginDlg.getLoggedInFullName(),
            loginDlg.getLoggedInRole()
        );
        mainWindow.show();
        return app.exec();
    }

    return 0;
}
