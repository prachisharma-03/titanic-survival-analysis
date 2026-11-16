import pandas as pd
import os
import matplotlib.pyplot as plt

# ---------- 1. LOAD ----------
df = pd.read_csv("data/titanic.csv")
print(df.shape)                      

# ---------- 2. INSPECT ----------
print(df.head())
print(df.isna().sum())              

# ---------- 3. CLEAN ----------
df["HasCabin"] = df["Cabin"].notna()
df = df.drop(columns=["Cabin"])
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
df["Age"] = df["Age"].fillna(
    df.groupby(["Sex", "Pclass"])["Age"].transform("median")
)

# ---------- 4. TIDY + NEW COLUMNS ----------
df["Survived"] = df["Survived"].astype(bool)
df["Embarked"] = df["Embarked"].map(
    {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}
)
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 12, 18, 60, 120],
    labels=["Child", "Teen", "Adult", "Senior"],
)

# ---------- 5. VERIFY ----------
print(df.shape)                      
print(df.isna().sum().sum())         
print(df.duplicated().sum())

# ---------- 6. QUESTIONS ----------

print("Q1. Overall survival rate:")
print(df["Survived"].mean())

print("\nQ2. Survival rate by sex:")
print(df.groupby("Sex")["Survived"].mean())

print("\nQ3. Survival rate by class:")
print(df.groupby("Pclass")["Survived"].mean())

print("\nQ4. Survival rate by age group:")
print(df.groupby("AgeGroup", observed=True)["Survived"].mean())

print("\nQ5a. Median fare by class:")
print(df.groupby("Pclass")["Fare"].median())

print("\nQ5b. Median fare, died vs survived:")
print(df.groupby("Survived")["Fare"].median())

# ---------- 7. CHARTS ----------
os.makedirs("outputs/charts", exist_ok=True)

# Chart 1: survival rate by sex
rates = df.groupby("Sex")["Survived"].mean()*100
rates.plot(kind="bar")
plt.title("Survival rate by sex")
plt.ylabel("Survived (%)")
plt.tight_layout()
plt.savefig("outputs/charts/survival_by_sex.png", dpi=150)
plt.close()

# Chart 2: survival rate by class
rates = df.groupby("Pclass")["Survived"].mean()*100
rates.plot(kind="bar")
plt.title("Survival rate by class")
plt.ylabel("Survived (%)")
plt.tight_layout()
plt.savefig("outputs/charts/survival_by_class.png", dpi=150)
plt.close()

# Chart 3: survival rate by age group
rates = df.groupby("AgeGroup")["Survived"].mean()*100
rates.plot(kind="bar")
plt.title("Survival rate by age group")
plt.ylabel("Survived (%)")
plt.tight_layout()
plt.savefig("outputs/charts/survival_by_Agegroup.png", dpi=150)
plt.close()
