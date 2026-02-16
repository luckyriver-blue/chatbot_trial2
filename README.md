本リポジトリは、チャットボットとの相談行為に関する実験実施のために開発した会話システムです。


## 目次

- [実験概要](#実験概要)
- [システム構成図と使用技術](#システム構成図と使用技術)
- [ディレクトリ構造](#ディレクトリ構造)


## 実験概要

本実験では、参加者は以下のいずれかの条件に割り当てられ、チャットボットと5分以上の会話を行った。

- ボットに相談する条件  
- ボットに浅く相談される条件  
- ボットに深く相談される条件  

本研究は、自己開示の返報性の観点から、ボットから（深く）相談を受ける状況が、ユーザーの自己開示意欲を高めるかどうかを検討することを目的とした。  
会話終了後、Qualtrics を用いてボットに対する将来的な自己開示意欲を測定し、条件間で比較分析を行った。


## システム構成図と使用技術
システム構成図
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/9c61a90e-c299-40b2-a09e-f519d0307353" />

使用技術
- 言語：Python
- LLM：[OpenAI API](#OpenAI-API) 
- LLM制御：[LangChain / LangGraph](#LangChainとLangGraph)
- データベース：[Firebase](#Firebase)
- フロントエンド：[Streamlit](#Streamlit)

### OpenAI API
  GPT系モデルを提供しているOpenAI社のLLMである。  
  実験参加者と会話するAIとして、このOpenAI APIを用い、その中のGPT-4oを使用した。  
  [OpenAI APIの公式ドキュメント](https://developers.openai.com/api/docs) 
   
### LangChainとLangGraph
  LangChain  
    LLMを利用したアプリケーション開発を支援するPythonのライブラリであり、プロンプトの管理、会話履歴の保持、LLMのモデル設定などを統合的に扱うことができる。  
    本システムでは、LangChainが提供するプロンプトテンプレート機能を利用し、LLMへの指示と会話履歴を組み合わせたプロンプトを入力するよう設計した。 
    
  LangGraph  
    LLMを用いた処理の流れをノードとエッジからなるグラフ構造で表現し、状態遷移に基づいて実行管理を行う、LangChainの拡張ライブラリである。
    各ノードには処理関数が定義され、グラフが実行されると、現在の状態を引数としてノード内の関数が呼び出され、処理結果が次の状態として返される。  
    本システムで構築したグラフは、LangChainで管理しているプロンプトを、設定したLLMに入力して応答を生成する単一ノードで構成されているが、生成された応答を添削するノードの追加や、条件分岐、繰り返しの処理の導入など、より複雑な拡張が可能である。
  
  [LangChainの公式ドキュメント](https://docs.langchain.com)

### Firebase
  データベースやストレージなど、アプリケーションのバックエンド機能を担うGoogleのクラウドサービスである。  
  本システムでは、Firebaseが提供するデータベースであるCloud Firestoreを利用し、人とチャットボットとの会話履歴をリアルタイムに保存をする設計とした。  
  [Firestoreの公式ドキュメント](https://firebase.google.com/docs/firestore?hl=ja)
    
  
### Streamlit
  Pythonによるフロントエンドを含むWebアプリケーション開発が可能なフレームワークである。  
  Streamlitを使用することで、開発言語をPythonに統一した。  
  [Streamlitの公式ドキュメント](https://docs.streamlit.io)
  

## ディレクトリ構造
talk_bot.pyでボット本体を制御し、main.pyで応答生成時、ボットを呼び出しています  
.  
├── .devcontainer/          
├── .streamlit/            &emsp;# Streamlit（フロントエンド）設定  
├── __pycache__/             
├── config/                &emsp;# API設定  
&emsp;├── set_llm.py          &emsp;# LLM（OpenAI API）の設定  
&emsp;└── set_firebase.py     &emsp;# Firebase（Firestore） 接続    
├── style_and_javascript/  &emsp;# Streamlit の UI    
&emsp;├── style.py             &emsp;# CSS  
&emsp;└── javascript.py        &emsp;# Javascript  
├── ***talk_bot.py             &emsp;# チャットボットのロジック本体（会話履歴・プロンプト管理）***  
├── ***main.py                 &emsp;# 会話システムの実行（UI、ChatBotなど呼び出し）***  
├── requirements.txt        &emsp;# 依存ライブラリ一覧  
├── Procfile                 &emsp;# Heroku デプロイ用設定  
├── .gitignore                 
└── README.md               
 
