from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
# Detect if score is over 0.5
def baseline(message):
    model_name = 'smilegate-ai/kor_unsmile'
    model = BertForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    pipe = TextClassificationPipeline(
            model = model,
            tokenizer = tokenizer,
            device = -1,   # cpu: -1, gpu: gpu number
            return_all_scores = True,
            function_to_apply = 'sigmoid'
        )
    
    for result in pipe(message)[0]:
        if result['label'] != "clean":
            if result['score'] >= 0.5:
                return result
    
    return None