from persistence.sqlite import FileHistoryDB

if __name__ == "__main__":
    db = FileHistoryDB()
    moves = db.get_all_moves()
    for move in moves:
        print(move)
    db.close()