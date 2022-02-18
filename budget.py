class Category:

    def __init__(self, category):
        self.ledger = []
        self.cat = category

    def get_balance(self):
        tot_ = 0
        for i in self.ledger:
            tot_ += i["amount"]
        return tot_

    def __str__(self):
        l = len(self.cat)
        star = int(30 - l)
        tit = "*" * int(star // 2) + self.cat.capitalize() + "*" * int(star - int(star // 2))
        string = ""
        tot = 0
        for i in self.ledger:
            tot += i["amount"]
            string += "%s" % (i["description"][:23])
            length = len(i["description"][:23])
            if length < 23:
                # string += "%s\n"%(str(i["amount"])[:7]).rjust(30 - length)
                string += "%s" % str("%.2f\n" % (i["amount"]))[:7].rjust(31 - length)
            else:
                # string += "%s\n"%(str(i["amount"])[:7]).rjust(7)
                string += "%s" % str("%.2f\n" % (i["amount"]))[:7].rjust(8)
        tit = tit + "\n" + string
        tit += "Total: " + str(tot)
        self.cat = str(self.cat)
        return tit

    def check_funds(self, amount):
        tot = 0
        for i in self.ledger:
            tot += i["amount"]
        tot -= amount
        if tot >= 0:
            return True
        elif tot < 0:
            return False

    def deposit(self, amount, category=str("")):
        dict_ = dict()
        dp_items = self.ledger
        dict_["amount"] = amount
        dict_["description"] = category
        dp_items.append(dict_)

    def withdraw(self, amount, category=str("")):
        dict_ = dict()
        dp_items = self.ledger
        dict_["amount"] = -1.0 * amount
        dict_["description"] = category
        if self.check_funds(amount):
            dp_items.append(dict_)
            return True
        else:
            return False

    def transfer(self, transfer_amount, obj):
        ls = str(obj)[0:30]
        los = [str(obj)[i] for i in range(0, 30) if str(obj)[i] != "*"]
        destination = "Transfer to " + str(''.join(los))
        if self.check_funds(transfer_amount):
            self.withdraw(transfer_amount, destination)
            obj.deposit(transfer_amount, category="Transfer from {}".format(str(self.cat)))
            return True
        else:
            return False

def create_spend_chart(a):

    tot_ = [j["amount"] for i in a for j in i.ledger if j["amount"] < 0]
    o = lambda i: round(i * 100.0 / sum(tot_) / 10.0)
    dot_ = [o(i) + 1 if o(i) > 1 else o(i) for i in tot_]
    string = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        string += "%s|" % str(i).rjust(3)
        for j in range(0, len(dot_)):
            l = int((dot_[j] - 1) * 10)
            if l == i:
                string += " " + "o" + " "
                dot_[j] -= 1
            else:
                string += "   "
        string += " \n"
    string += "    " + "-" * ((len(a)*3)+1) + "\n"
    k1 = [str(a[k].cat).capitalize() for k in range(0, len(a))]
    k2 = [len(k) for k in k1 ]
    for i in range(0, max(k2)):
        string += " "*4
        for w in k1:
            try:
                string += " " + w[i] + " "
            except Exception:
                string += "   "
        if i < (max(k2)-1):
            string += " \n"
        else:
            string += " "
    return string
