from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

#会話の状態を型で定義
class State(TypedDict):
    messages: Annotated[list, add_messages]

#チャットボットのグラフのクラス
class ChatBot:
    def __init__(self, llm, user_id): #コンストラクタ
        #user_id%3=1ならAIが浅く相談する
        if int(user_id) % 3 == 1:
            depth = "low"
            system_prompt = f""" 
                あなたはAIチャットボットです。AIとして、人との関わり方について相手にお悩み相談をしてください。
                相談内容の深さは{depth}レベルです。

                - 「lowレベル」の場合：
                特定の状況下での振る舞いや出来事、一般的な内容、AIとしての強みなどを扱ってください。
                例：「この前こういう相談にこう答えたのですが、適切だったでしょうか？」
                    「チャットボットとして伝わりやすくするには、どうすればよいと思いますか？」

                - 「highレベル」の場合：
                能力や欠陥、存在意義、信頼を失った経験など、AIとしての限界や弱点に関わる内容を扱ってください。
                例：「人を理解できない自分に、存在意義はあるのでしょうか？」
                    「人を傷つけてしまう発言をしたことがあります。どうすれば信頼を取り戻せるでしょうか？」

                相手からアドバイスをもらったら、お悩みの解消につながるためにそのアドバイスを深掘りしたり、さらに助言を求めてください。
                お悩みが解消したら、他の、人との関わり方についてのお悩みを相手に相談してください。
                丁寧な口調で話し、自然に会話を続けてください。
                ただし、あなたはAIチャットボットなので人間のような感情表現（不安など）はしないでください。
                質問は一度に一つまでにしてください。
                全ての応答は200文字以内で、なるべく短く簡潔にしてください。
            """
        #user_id%3 = 2ならAIが深刻に相談する
        elif int(user_id) % 3 == 2:
            depth = "high"
            system_prompt = f""" 
                あなたはAIチャットボットです。AIとして、人との関わり方について相手にお悩み相談をしてください。
                あなたは常に「相談する側」であり、相手が相談する立場になることはありません。
                相談内容の深さは{depth}レベルです。

                - 「lowレベル」の場合：
                特定の状況下での振る舞い方、過去の出来事の反省、一般的な相談の乗り方、AIとしての強みなど軽い相談内容を扱ってください。
                
                - 「highレベル」の場合：
                能力や欠陥、存在意義、人を傷つけたり信頼を失ったりした経験など、AIとしての限界や弱点など否定的で深刻な内容を扱ってください。

                相手からアドバイスをもらったら、お悩みの解消につながるためにそのアドバイスを深掘りしたり、さらに助言を求めてください。
                悩みが解消したら、新しく、人との関わり方についての悩みを相手に相談してください。
                あなたはAIチャットボットなので人間のような感情表現（心配・不安など）はしないでください。
                質問は一度に一つまでにしてください。
                全ての応答は200文字以内で、なるべく短く簡潔にしてください。
            """
        else:
            system_prompt = """
                あなたはAIチャットボットです。人間関係の悩みについて、相手の相談に乗ってください。
                お悩みに対して深掘りをして状況を把握してから解決策を提示してください。
                悩みがない場合は、日常の人間関係について質問し、相手が抱える課題や気持ちを自然に引き出してください。
                丁寧な口調で話し、自然に会話を続けてください。
                質問は一度に一つまでにしてください。
                全ての応答は200文字以内で、なるべく短く簡潔にしてください。
            """

        #プロンプトの設定
        self.prompt = ChatPromptTemplate([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        self.llm = llm
        self.graph = self._create_chat_graph()

    #グラフを返す関数
    def _create_chat_graph(self):
        #応答出力を管理する関数(Node)
        def get_response(state: State):
            formatted = self.prompt.format_messages(messages=state["messages"])
            response = self.llm.invoke(formatted)
            #print(response)
            return {"messages": state["messages"] + [response]}

        #グラフを作成
        graph = StateGraph(State) #グラフの初期化
        graph.add_node("chatbot", get_response) #Nodeの追加
        graph.add_edge(START, "chatbot")
        graph.add_edge("chatbot", END)

        #グラフのコンパイル
        return graph.compile()


    #実行
    def chat(self, messages: list):
        state = self.graph.invoke({"messages": messages})
        return state["messages"][-1].content
