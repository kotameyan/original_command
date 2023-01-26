#!/bin/sh

# 入力した特殊キーを判別してくれる関数
capture_special_keys(){
    local SELECTION rest
    IFS= read -r -n1 -s SELECTION
    if [[ $SELECTION == $'\x1b' ]]; then
        read -r -n2 -s rest
        SELECTION+="$rest"
    else
        case "$SELECTION" in
            "")
                echo "Enter"
                ;;
            $'\x7f')
                echo "Backspace"
                ;;
            $'\x20')
                echo "Space"
                ;;
            *)
                read -i "$SELECTION" -e -r rest
                echo "$rest"
                ;;
        esac
        return 0
    fi

    case $SELECTION in
        # backspace 
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
    esac
}

# 実行するpythonファイルのリストを取得
files=($(ls -t -1 *.py))

# filesの要素の最後尾を取得
end_elem=$((${#files[@]}-1))

# 現在選択されている項目の番号を記憶する変数（最初は一番上が選択されている）
selected=0

# 項目を選択する
while true
do
    # 画面をクリアし、選択画面の表示を準備
    echo "\033[f"
    echo "\033[2J"
    echo "\033[2A"

    # 選択画面を表示する
    for i in ${!files[@]}
    do
        if [ $i -eq $selected ]; then
            echo "\033[7m ${files[$i]} \033[0m"
        else
            echo "${files[$i]}"
        fi
    done

    # キー入力を受け入れる
    key="$(capture_special_keys)"
    # echo $key

    # ↑キーで選択しているものを上にずらす
    if [ $key = "Up" ]; then
        if [ $selected -gt 0 ]; then
            selected=$(($selected-1))
        fi
    fi

    # ↓キーで選択しているものを下にずらす
    if [ $key = "Down" ]; then
        if [ $selected -lt $end_elem ]; then
            selected=$(($selected+1))
        fi
    fi

    # エンターで選択を決定する
    if [ "$key" = "Enter" ]; then
        break
    fi
done

# 選択したPythonファイルを実行
echo ""
echo "python3 ${files[$selected]}"
echo "----------------------------------------"
python3 ${files[$selected]}