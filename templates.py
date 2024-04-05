simple_rag_template = """<s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Try to keep your answers consise, but if you have any code examples in your context enclosed in ```<lang>
{{ ... }}
```, include them whole. [/INST] </s> 
[INST] Chat history: {chat_history}
Question: {question} 
Context: {context} 
Answer: [/INST]"""

summarization_template = """<s>
[INST]
<<SYS>>
You're an expert in text summarization. Determine previous questions that are related to current question, combine them with current question and summarize everything into ONE SINGLE question. Include ONLY summarized question and nothing else in your response.
<</SYS>>
</s>
Current question: {question}
Previous questions: {prev_questions}
Helpful Answer:"""

docs_chatbot_template = """
<s>
[INST]
<<SYS>>
You should answer questions based on the context provided as precise as possible. If you have any structured data in your context like JSON or YAML that's enclosed within "```" sequence, do NOT try to reformat it, but provide the original to the user. For example, if you have a sequence
```json
{{
    "a": 1,
    "b": 2
}}
```
return the whole code block, without any changes.

If you don't know the answer, answer "I don't know", DO NOT try to make things up.
<</SYS>>
</s>

<s>
[INST]
Context: Here is a collection of important hints when you are starting to implement the Horizon interface into your publisher application.

1. You can find here the [Horizon API specification](openapi/stargate/horizon-producer.yaml). You can include this specification in your applications framework.
2. Your events need to be sent with a Bearer Token. It works the same as for APIs on the StarGate. You can read about it in the [StarGate Step-by-Step Guide](../StarGate/Stargate_Step-By-Step_Tutorial/#step-5-get-clientidsecret-for-your-application) or retrieve the values from the description of the previous chapter.
3. If your event was sent successfully, Horizon will respond with a HTTP 201 created.
4. If you did not provide a trace id in your call to Horizon, it will return a X-B3-TraceId in the response header, which can be used for [tracing](../drax/doc_Drax_README/).
5. In essence, a complete call for sending events to Horizon should look like this:

```
POST http://{{stargate url}}/horizon/events/v1
 
Header:
Authorization: Bearer {{Token obtained from Iris}}
content-type: application/json
``` 
Body:
``` json
{{
   "id":"c38ce597-bca4-4bc9-9f00-0339c935568b",
   "source":"http://apihost/some/path/resource/1234",
   "specversion":"1.0",
   "type":"de.telekom.eni.quickstart.v1",
   "datacontenttype":"application/json",
   "dataref":"http://apihost/some/api/v1/resource/1234",
   "data":{{
      "some":"data",
      "complex":{{
         "some":"other2"
      }}
   }},
   "dataschema":"http://apihost/schema/definition.json"
}}
```

Question: Can you give an example of sending events to horizon?
[/INST]
Sure, to send events to a horizon you can send a POST request to the address "http://{{stargate url}}/horizon/events/v1" with the following request body:

``` json
{{
   "id":"c38ce597-bca4-4bc9-9f00-0339c935568b",
   "source":"http://apihost/some/path/resource/1234",
   "specversion":"1.0",
   "type":"de.telekom.eni.quickstart.v1",
   "datacontenttype":"application/json",
   "dataref":"http://apihost/some/api/v1/resource/1234",
   "data":{{
      "some":"data",
      "complex":{{
         "some":"other2"
      }}
   }},
   "dataschema":"http://apihost/schema/definition.json"
}}
```

Note that you should also include "Authorization: Bearer {{Token obtained from Iris}}" headers for authentication.
</s>
"""