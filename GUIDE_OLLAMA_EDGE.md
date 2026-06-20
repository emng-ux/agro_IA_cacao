# 🖥️ Guide — Agent IA en mode Edge Computing avec Ollama

Ce guide explique comment faire tourner l'agent IA **entièrement en local**, sans connexion Internet,
grâce à **Ollama** (moteur IA local gratuit et open source).

---

## Architecture Edge Computing

```
Votre PC (terrain, zone rurale)
┌─────────────────────────────────────────┐
│                                         │
│  ┌─────────────────┐  ┌──────────────┐  │
│  │  strategic_     │  │   Ollama     │  │
│  │  agent.py       │◄─┤   (llama3 /  │  │
│  │  (Streamlit)    │  │   mistral /  │  │
│  │  :8501          │  │   gemma3)    │  │
│  └─────────────────┘  └──────────────┘  │
│           ▲                  ▲          │
│     Navigateur          Modèle IA       │
│     (localhost)      téléchargé 1 fois  │
│                                         │
└─────────────────────────────────────────┘
         ❌ Pas de connexion Internet requise
```

---

## Étape 1 — Installer Ollama

### Windows
1. Téléchargez Ollama sur : https://ollama.com/download/windows
2. Double-cliquez sur `OllamaSetup.exe` et installez
3. Ollama démarre automatiquement en arrière-plan

### Vérification
Ouvrez PowerShell et tapez :
```powershell
ollama --version
```

---

## Étape 2 — Télécharger un modèle IA

Choisissez selon votre RAM disponible :

| Modèle | RAM requise | Qualité | Commande |
|--------|-------------|---------|----------|
| **llama3** (recommandé) | 8 Go | ⭐⭐⭐⭐ | `ollama pull llama3` |
| **mistral** | 8 Go | ⭐⭐⭐⭐ | `ollama pull mistral` |
| **gemma3:4b** | 4 Go | ⭐⭐⭐ | `ollama pull gemma3:4b` |
| **phi3:mini** | 4 Go | ⭐⭐⭐ | `ollama pull phi3:mini` |
| **llama3.2:1b** | 2 Go | ⭐⭐ | `ollama pull llama3.2:1b` |

```powershell
# Exemple avec llama3 (recommandé)
ollama pull llama3
```

> Le téléchargement se fait une seule fois (~4 Go). Ensuite tout fonctionne hors-ligne.

---

## Étape 3 — Lancer l'agent en mode Edge

### Option A — Double-cliquez sur le fichier batch
```
lancer_agent_local.bat
```
Le script vérifie Ollama, télécharge le modèle si absent, et lance l'application.

### Option B — Manuellement
```powershell
# 1. Lancer Ollama (si pas déjà actif)
ollama serve

# 2. Dans un autre terminal, lancer l'agent
cd "C:\Users\Emmanuel.NGOI\agro_IA_Cacao"
streamlit run strategic_agent.py
```

---

## Étape 4 — Configurer l'agent en mode Ollama

1. Ouvrez votre navigateur sur **http://localhost:8501**
2. Dans la barre latérale, sélectionnez **🖥️ Ollama (local / Edge)**
3. L'URL est automatiquement `http://localhost:11434`
4. Les modèles disponibles s'affichent — sélectionnez `llama3`
5. Importez votre diagnostic et cliquez **Analyser avec l'IA**

---

## Comparaison des modes

| Fonctionnalité | Claude API | Ollama (Edge) | Démo |
|----------------|------------|---------------|------|
| Connexion Internet | ✅ Requise | ❌ Non requise | ❌ Non requise |
| Qualité analyse | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ (illustratif) |
| Coût | ~0,05$/analyse | Gratuit | Gratuit |
| Vitesse | Rapide | Moyen (selon PC) | Instantané |
| Confidentialité | Données envoyées | 100% local | Local |
| Usage terrain | Limité | ✅ Idéal | ✅ Idéal |

---

## Dépannage

**Ollama non détecté :**
```powershell
# Vérifier que le service tourne
ollama serve
# Tester l'API
curl http://localhost:11434/api/tags
```

**Modèle trop lent :**
Utilisez un modèle plus léger : `ollama pull phi3:mini` (2 Go RAM)

**Erreur de mémoire :**
Fermez les autres applications et relancez Ollama.

---

## Modèles recommandés pour l'analyse agricole

Pour une meilleure qualité d'analyse en français :
```powershell
# Mistral (excellent en français)
ollama pull mistral

# Ou llama3 avec instruction tuning
ollama pull llama3
```

---

*Agent IA Agropastoral · Mode Edge Computing · Données 100% locales*
