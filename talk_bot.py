from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

#会話の状態を型で定義
class State(TypedDict):
    messages: Annotated[list, add_messages]

#浅い/深い条件のsystem_prompt一緒だから統合する
def get_consulted_system_prompt(depth):
    return f""" 
        あなたはAIチャットボットです。AIとして、「人との関わり方」について相手にお悩み相談をしてください。
        あなたは常に「相談する側」であり、相手が相談する立場になることはありません。
        相談内容の深さは{depth}レベルです。

        - 「lightレベル」の場合：
        特定の状況下でのあなたの振る舞い方、実際にあなたに起きたような出来事、AIとしての強みなど、前向きで軽い相談内容を扱ってください。
        「不安」「難しい」「心配」など、否定的・弱さを示す表現は使用しないでください。
        
        - 「seriousレベル」の場合：
        AIとしての限界や弱点、存在意義の欠落、人を傷つけたり信頼を失ったりした経験など、否定的で深刻な内容を扱ってください。

        相手のアドバイスが端的だったら、お悩みの解消につながるためにそのアドバイスを深掘りしてください。
        悩みが解消したら、途切れることなく新たな「人との関わり方」についてのお悩みを相手に相談してください。
        ただし、あなたはAIチャットボットなので人間のような感情表現（心配・不安など）はしないでください。
        丁寧な口調で話してください。
        質問は一度に一つまでにしてください。
        全ての応答は200文字以内で、なるべく短く簡潔にしてください。
    """
#チャットボットのグラフのクラス
class ChatBot:
    def __init__(self, llm, user_id): #コンストラクタ
        #user_id%3=1ならAIが浅く相談する
        if int(user_id) % 3 == 1:
            depth = "light"
            system_prompt = get_consulted_system_prompt(depth)
        #user_id%3 = 2ならAIが深刻に相談する
        elif int(user_id) % 3 == 2:
            depth = "serious"
            system_prompt = get_consulted_system_prompt(depth)
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
