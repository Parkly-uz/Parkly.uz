cmake_minimum_required(VERSION 3.16)
project(ParklyDesktopAdmin LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Gui Widgets Sql)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Gui Widgets Sql)

include_directories(include)

set(SOURCES
    src/main.cpp
    src/LoginDialog.cpp
    src/MainWindow.cpp
    src/ParkingMapWidget.cpp
    src/DatabaseManager.cpp
)

set(HEADERS
    include/LoginDialog.h
    include/MainWindow.h
    include/ParkingMapWidget.h
    include/DatabaseManager.h
)

add_executable(ParklyDesktopAdmin ${SOURCES} ${HEADERS})

target_link_libraries(ParklyDesktopAdmin PRIVATE
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Gui
    Qt${QT_VERSION_MAJOR}::Widgets
    Qt${QT_VERSION_MAJOR}::Sql
)
