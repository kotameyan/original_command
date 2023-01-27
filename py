#!/usr/bin/env bash

# --------------------------関数定義--------------------------
# 特殊キーを認識する関数
CaptureSpecialKeys(){
    local SELECTION rest

    IFS= read -r -n1 -s SELECTION
    #echo "$SELECTION" | hexdump >&2
    if [[ $SELECTION == $'\x1b' ]]; then
        read -r -n2 -s rest
        SELECTION+="$rest"
    else
        if [[ "$SELECTION" == '' ]] ;then
            echo "Enter"
            return 0
        else
            read -r rest
            echo "$SELECTION$rest"
            return 0
        fi
    fi


    case $SELECTION in
        $'\x1b\x5b\x41') #up arrow
            echo "Up"
            ;;
        $'\x1b\x5b\x42') #down arrow
            echo "Down"
            ;;
        $'\x1b\x5b\x43') #right arrow
            echo "Right"
            ;;
        $'\x1b\x5b\x44') #left arrow
            echo "Left"
            ;;
        $'\x20') #space
            echo "Space"
            ;;
    esac
}

# エスケープシーケンスを用いた関数
ClearScreen(){
    printf "\033[2J"
}
ClearRight(){
    printf "\033[0K"
}
ClearLeft(){
    printf "\033[1K"
}
ClearLine(){
    printf "\033[2K"
}
MoveCursor(){
    printf "\033[%d;%dH" "$1" "$2"
}
MoveCursorUp(){
    printf "\033[%dA" "$1"
}
MoveCursorDown(){
    printf "\033[%dB" "$1"
}
MoveCursorRight(){
    printf "\033[%dC" "$1"
}
MoveCursorLeft(){
    printf "\033[%dD" "$1"
}
SaveCursor(){
    printf "\033[s"
}
ResetStyle(){
    printf "\033[0m"
}
ClearUpperLines(){
    for i in $(seq 1 "$1"); do
        MoveCursorUp 1
        ClearLine
    done
}

# メニューを表示する関数
ShowMenu(){
    for i in "${!Choices[@]}"; do
        if [[ "$i" = "$CurrentChoice" ]]; then
            printf "\033[47m${Choices[$i]}\033[0m\n"
        else
            printf " ${Choices[$i]} \n"
        fi
    done
}

# メニューを更新する関数
UpdateMenuScreen(){
    ClearUpperLines "${#Choices[@]}"
    ShowMenu
}

# メニューを生成する関数
GenerateMenu(){
    # 実行するpythonファイルのリストを取得
    Choices=(${1})

    # 何番目が指定されているか記憶する変数を作成
    CurrentChoice=0

    # 入力したキーを受け取る変数を作成
    Key=""

    # メニューを表示する
    ShowMenu

    # カーソルを非表示にする
    printf "\033[?25l"

    # メニューの中から項目を選択する
    while [[ -z "$Key" ]]; do
        Key="$(CaptureSpecialKeys)"
        case "$Key" in
            Up)
                if (( "$CurrentChoice" != 0 )); then
                    CurrentChoice=$((CurrentChoice - 1))
                    UpdateMenuScreen
                fi
                ;;
            Down)
                if (( "$CurrentChoice" != "${#Choices[@]}" - 1 )); then
                    CurrentChoice=$((CurrentChoice + 1))
                    UpdateMenuScreen
                fi
                ;;
            Enter)
                break
                ;;
        esac
        Key=""
    done 

    # カーソルを表示する
    printf "\033[?25h"

    # 選択メニューを削除
    for i in "${!Choices[@]}"; do
        MoveCursorUp
        ClearLine
    done

    # 選択された項目
    # ${Choices[$CurrentChoice]}
}



# --------------------------処理--------------------------
# 実行するpythonファイルのリストを取得
files=($(ls -t -1 *.py))

#選択メニューを展開
GenerateMenu "${files[*]}"

# 選択したPythonファイルを実行
echo ""
echo "python3 ${Choices[$CurrentChoice]}"
echo "----------------------------------------"
python3 ${Choices[$CurrentChoice]}

# Referred to the following sites
# https://gist.github.com/Hayao0819/d7554f55ccd84a53b5973764497d5714