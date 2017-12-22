import numpy as np
import mxnet as mx
import argparse
import read_music
parser = argparse.ArgumentParser(description="Train RNN on Penn Tree Bank",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--num-layers', type=int, default=2,
                    help='number of stacked RNN layers')
parser.add_argument('--num-hidden', type=int, default=200,
                    help='hidden layer size')
parser.add_argument('--num-embed', type=int, default=200,
                    help='embedding layer size')
parser.add_argument('--gpus', type=str,
                    help='list of gpus to run, e.g. 0 or 0,2,5. empty means using cpu. ' \
                         'Increase batch size when using multiple gpus for best performance.')
parser.add_argument('--kv-store', type=str, default='device',
                    help='key-value store type')
parser.add_argument('--num-epochs', type=int, default=2,
                    help='max num of epochs')
parser.add_argument('--lr', type=float, default=0.01,
                    help='initial learning rate')
parser.add_argument('--optimizer', type=str, default='sgd',
                    help='the optimizer type')
parser.add_argument('--mom', type=float, default=0.0,
                    help='momentum for sgd')
parser.add_argument('--wd', type=float, default=0.00001,
                    help='weight decay for sgd')
parser.add_argument('--batch-size', type=int, default=16,
                    help='the batch size.')
parser.add_argument('--disp-batches', type=int, default=25,
                    help='show progress for every n batches')


def tokenize_pitch(fname,invalid_label=-1,start_label=0):
    pitch = np.load('npdata/pitch.npy').tolist()
    start = np.load('npdata/start.npy').tolist()
    end = np.load('npdata/end.npy').tolist()
    res=[]
    for each in range(0,len(pitch)):
        res.append(pitch[each]+start[each]+end[each])
    return res

def tokenize_pitch_as_sentences(pathname , vocab=None,invalid_label=-1,start_label=0):
    notes = read_music.read_midi(pathname)
    sentence = read_music.note2sentences(notes)
    sentences, vocab = mx.rnn.encode_sentences(sentence, vocab=vocab, invalid_label=invalid_label,
                                           start_label=start_label)
    return sentences, vocab

if __name__ == '__main__':
    import logging
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=head)

    args = parser.parse_args()

    #buckets = []
    buckets = [2, 4, 8, 16, 32]

    start_label = 1
    invalid_label = -1
    vocab_space = 64

    train_sent, vocab = tokenize_pitch_as_sentences("Minuet-in-G-Minor.mid",vocab=None)

    data_train  = mx.rnn.BucketSentenceIter(train_sent, args.batch_size,
                                            invalid_label=invalid_label)
    stack = mx.rnn.SequentialRNNCell()
    for i in range(args.num_layers):
        stack.add(mx.rnn.LSTMCell(num_hidden=args.num_hidden, prefix='lstm_l%d_'%i))

    def sym_gen(seq_len):
        data = mx.sym.Variable('data')
        label = mx.sym.Variable('softmax_label')
        embed = mx.sym.Embedding(data=data, input_dim=vocab_space,
                                 output_dim=args.num_embed, name='embed')

        stack.reset()
        outputs, states = stack.unroll(seq_len, inputs=embed, merge_outputs=True)

        pred = mx.sym.Reshape(outputs, shape=(-1, args.num_hidden))
        pred = mx.sym.FullyConnected(data=pred, num_hidden=vocab_space, name='pred')

        label = mx.sym.Reshape(label, shape=(-1,))
        pred = mx.sym.SoftmaxOutput(data=pred, label=label, name='softmax')

        return pred, ('data',), ('softmax_label',)

    if args.gpus:
        contexts = [mx.gpu(int(i)) for i in args.gpus.split(',')]
    else:
        contexts = mx.cpu(0)

    model = mx.mod.BucketingModule(
        sym_gen             = sym_gen,
        default_bucket_key  = data_train.default_bucket_key,
        context             = contexts)

    model.fit(
        train_data          = data_train,
        # eval_data           = data_val,
        eval_metric         = mx.metric.Perplexity(invalid_label),
        kvstore             = args.kv_store,
        optimizer           = args.optimizer,
        optimizer_params    = { 'learning_rate': args.lr,
                                'momentum': args.mom,
                                'wd': args.wd },
        initializer         = mx.init.Xavier(factor_type="in", magnitude=2.34),
        num_epoch           = args.num_epochs,
        batch_end_callback  = mx.callback.Speedometer(args.batch_size, args.disp_batches))

    res = model.get_outputs(True)[0].asnumpy()
    print(res)
    print(res.shape)