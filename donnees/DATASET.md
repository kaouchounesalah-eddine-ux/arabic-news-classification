# Jeu de données — Catégorisation automatique d'articles (arabe)

Ce dossier fournit le corpus de travail pour le PFA.

## Fichiers
- **`articles.sample.json`** — un petit échantillon (15 articles) qui illustre le **schéma** et sert à mettre au point le pipeline (smoke tests). ⚠️ Trop petit pour entraîner un vrai modèle.
- **`articles.json`** — le **corpus complet** (des milliers d'articles étiquetés), **fourni par l'encadrant**. C'est le fichier qui sert à l'entraînement et à l'évaluation. Il se charge **exactement comme l'échantillon** (même schéma).
- **`export_articles.sh`** — le script qui a servi à générer `articles.json` (pour information). **Tu n'as pas besoin de l'exécuter.**
- **`DATASET.md`** — ce fichier.

## Schéma d'un article
```json
{
  "id": "art-0001",                       // identifiant unique (chaîne)
  "title": "…",                           // titre de l'article
  "content": "…",                         // texte brut de l'article (features)
  "categories": ["سياسة", "اقتصاد"],      // 1..N catégories (labels) — peut être multi-label
  "publishedAt": "2026-03-04"             // date de publication (YYYY-MM-DD)
}
```

## Charger les données (Python)
```python
import json, pandas as pd

# 1) échantillon (mise au point du code)
sample = json.load(open("articles.sample.json", encoding="utf-8"))

# 2) corpus complet (entraînement / évaluation) — fourni par l'encadrant
data = json.load(open("articles.json", encoding="utf-8"))
df = pd.DataFrame(data)     # colonnes : id, title, content, categories, publishedAt
```

## Notes importantes pour la modélisation
- **`content`** = les *features* (le texte à classer). **`categories`** = les *labels* (à prédire).
- **Multi-label :** un article peut appartenir à **plusieurs** catégories. Deux approches :
  1. *Single-label* pour commencer — prendre `categories[0]` comme étiquette unique.
  2. *Multi-label* (extension) — prédire l'ensemble (`MultiLabelBinarizer` + `OneVsRest`).
- **Déséquilibre de classes :** les catégories ne sont pas également représentées → penser `stratify`, `class_weight`, métrique **F1 macro** (pas seulement l'accuracy).
- **Arabe :** prévoir une étape de **normalisation** (ألف/همزة/تاء مربوطة), suppression des *stop-words*, et éventuellement *stemming* (CAMeL Tools / Farasa).

## Découpage conseillé
- `train` / `validation` / `test` avec **stratification** sur la catégorie.
- Garder un jeu de test **jamais vu** pour l'évaluation finale + la matrice de confusion.

---

### Note pour l'encadrant (génération de `articles.json`)
Le corpus complet est produit une seule fois par l'encadrant (le stagiaire ne reçoit **pas** l'accès à la base) :
```bash
export DATABASE_URL="postgresql://user:pass@host:5432/db"
./export_articles.sh            # -> articles.json (articles publiés, avec texte et ≥1 catégorie)
```
Le fichier `articles.json` obtenu est ensuite placé dans ce dossier et transmis au stagiaire.
