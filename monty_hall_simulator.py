from random import randint
import sys

class MontyHallLottery:
    def __init__(self):
        self.refresh_lottery()

    def refresh_lottery(self):
        self.doors = ['Goat', 'Goat', 'Goat']
        self.doors[randint(0, 2)] = 'Car'
        self.car_doors = []  # リストを初期化
        self.goat_doors = []  # リストを初期化
        # リストを作成
        for offset in range(3):
            if self.doors[offset] == 'Car':
                self.car_doors.append(offset)
            else:
                self.goat_doors.append(offset)

        self.selection = None
        self.opened = None
        self.ended = False

    def select(self, selection):
        self.selection = selection
        return self.selection

    def get_selection(self):
        return self.selection

    def show_one_goat_door(self):
        if self.selection is None:
            return None

        if self.doors[self.selection] == 'Car':
            # 残りのヤギドアからランダムに1つを返す
            self.opened = self.goat_doors[randint(0, len(self.goat_doors) - 1)]
        else:
            # 選んでいないヤギドアを返す
            self.opened = self.goat_doors[0] if self.selection != self.goat_doors[0] else self.goat_doors[1]

        return self.opened

    def change_selection(self):
        if self.selection is None or self.opened is None:
            return -1

        available_doors = set(range(3)) - {self.selection, self.opened}
        self.selection = available_doors.pop()
        return self.selection

    def show_result(self):
        if self.selection is not None:
            self.ended = True
            return self.doors[self.selection]
        return None

    def get_door_status(self):
        result = ''
        for offset in range(3):
            if self.opened == offset:
                result = result + '[GOAT]'
            elif (self.car_doors[0] == offset and self.ended):
                result = result + '[CAR ]'
            elif self.selection == offset:
                result = result + '[CHSN]'
            else:
                result = result + '[****]'
        return result

# 実行フェーズ
def run_simulation(change_selection, trial_times):
    mhl = MontyHallLottery()
    win = 0
    lose = 0
    result = ''

    # まず1行出力
    print()


    for wCnt in range(trial_times):
        # 初期化
        mhl.refresh_lottery()

        # ドア選択１回目
        mhl.select(randint(0, 2))

        # MontyHallがドアを１つ開ける
        mhl.show_one_goat_door()

        # ドアを変えるか？
        if change_selection:
            mhl.change_selection()
        else:
            mhl.get_selection()

        #結果を取得
        result = mhl.show_result()

        if result == 'Car':
            win += 1
        else:
            lose += 1

    # 結果を返す
    return f'選択変更：{"Yes" if change_selection else "No"}、試行回数：{trial_times}回、勝数：{win}、負数：{lose}、勝率：{win / ( win + lose ) : .3f}'

# 変更する場合
print(run_simulation(change_selection=True, trial_times=1000000))

# 変更しない場合
print(run_simulation(change_selection=False, trial_times=1000000))
