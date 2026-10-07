#pragma once

#include <QDialog>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QCheckBox>

class LoginDialog : public QDialog {
    Q_OBJECT

public:
    explicit LoginDialog(QWidget *parent = nullptr);

    QString getLoggedInUsername() const { return m_username; }
    QString getLoggedInFullName() const { return m_fullName; }
    QString getLoggedInRole() const { return m_role; }

private slots:
    void onLoginClicked();

private:
    QLineEdit *m_usernameEdit;
    QLineEdit *m_passwordEdit;
    QCheckBox *m_rememberCheck;
    QLabel *m_errorLabel;
    QPushButton *m_loginButton;

    QString m_username;
    QString m_fullName;
    QString m_role; // "SUPER_ADMIN", "ADMIN", "OPERATOR"

    void setupUI();
};
