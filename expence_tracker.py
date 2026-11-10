import argparse
import json
from datetime import datetime
import csv


def load_expenses():
    try:
        with open ("expences.json","r")as file:
            data=json.load(file)
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
         print("Error: The JSON file contains invalid data.")
         return []
def save_expenses(expenses):
    with open("expences.json","w") as file:
        json.dump(expenses,file)

def add_expense(description,amount,category):
    if amount <= 0:
        print("Error: Expense amount must be greater than zero.")
        return
    if not description.strip():
        print("Error: Description cannot be empty.")
        return

    if not category.strip():
        print("Error: Category cannot be empty.")
        return
    

    expenses=load_expenses()
    expense_id=max([expense["id"] for expense in expenses],default=0)+1
    today_date=datetime.now().strftime("%Y-%m-%d")
    new_expenses={
        "id":expense_id,
        "date":today_date,
        "description":description,
        "amount":amount,
        "category":category

    }
    expenses.append(new_expenses)
    save_expenses(expenses)
    print("successfully updated into the json file")
def list_expenses(category=None):
    expenses=load_expenses()
    if category is not None:
        expenses=[exp for exp in expenses if exp.get("category", "Uncategorized")==category]
    if not expenses:
        print("expenses is empty")
        return
    for exp in expenses:
        print(f"{exp['id']:<5}{exp['date']:<15}{exp['description']:<20}{exp['amount']:<10}{exp.get('category','Uncategorized'):<15}")
    
def delete_expense(expense_id):
    expenses=load_expenses()
    for exp in expenses:
        if exp["id"] ==expense_id:
            expenses.remove(exp)
            save_expenses(expenses)
            print("deletion done")
            break

    else:        
        print("no such expenses are seen in this")
            

def update_expense(expenses_id,description=None,amount=None):
    if description is not None and not description.strip():
        print("Error: Description cannot be empty.")
        return

    if amount is not None and amount <= 0:
        print("Error: Amount must be greater than zero.")
        return
    expenses=load_expenses()
    for expense in expenses:
        if expense["id"]==expenses_id:
            if description is not None:
                expense["description"]=description
            if amount is not None:
                expense["amount"]=amount
            save_expenses(expenses)
            print("updated successfully")
            break
    else:
        print("no such expense found")
def summary_expenses():
    expenses=load_expenses()
    amount_list= [expense["amount"] for expense in expenses]
    total_sum=sum(amount_list)
    print(f"total expenses is {total_sum}")
def monthly_summary(month,budget=None):
    if month < 1 or month > 12:
        print("Error: Month must be between 1 and 12.")
        return
    if budget is not None and budget < 0:
        print("Error: Budget cannot be negative.")
        return
    expenses=load_expenses()
    current_year=datetime.now().year
    matching_amount=[]
    for exp in expenses:
       date=datetime.strptime( exp['date'],"%Y-%m-%d")
       if date.month==month and date.year==current_year:
           matching_amount.append(exp['amount'])
    total_sum=sum(matching_amount)
    print(total_sum)
    if budget is None:
        print("budget is not provided")
    elif budget==total_sum:
        print("you meet your budget")
    elif budget>total_sum:
        print(f"your remaining balance is {budget-total_sum}")
    elif budget<total_sum:
        print(f"you are exceeding your limit{total_sum-budget}")

def export_expenses():
    expenses=load_expenses()
    
    with open("expenses.csv","w",newline="",encoding="utf-8")as file:
        dict_writer=csv.DictWriter(file,["id","date","description","amount","category"])
        dict_writer.writeheader()
        dict_writer.writerows(expenses)
      


        

   
def create_parser():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", type=str, required=True)
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", type=str, required=True)
    list_parser=subparsers.add_parser("list")
    list_parser.add_argument("--category",type=str)
    delete_parser=subparsers.add_parser("delete")
    delete_parser.add_argument("--id",type=int,required=True)
    update_parser=subparsers.add_parser("update")
    update_parser.add_argument("--id",type=int,required=True)
    update_parser.add_argument("--description",type=str,required=False)
    update_parser.add_argument("--amount",type=float,required=False)
    summary_parser=subparsers.add_parser("summary")
    monthly_summary_parser=subparsers.add_parser("monthly-summary")
    monthly_summary_parser.add_argument("--month",type=int,required=True)
    monthly_summary_parser.add_argument("--budget",type=float,)
    subparsers.add_parser("export")

    




    return parser


def main():
    parser=create_parser()
    args=parser.parse_args()
    if args.command=="add":
        add_expense(args.description,args.amount,args.category)
        return
    elif args.command=="list":
        list_expenses(args.category)
        return
    elif args.command=="delete":
        delete_expense(args.id)
        return
    elif args.command=="update":
        update_expense(args.id,args.description,args.amount)
    elif args.command=="summary":
        summary_expenses()
    elif args.command=="monthly-summary":
        monthly_summary(args.month,args.budget)
    elif args.command=="export":
            export_expenses()
if __name__ == "__main__":
    main()


