package main

import (
	"bufio"
	"io"
	"os"
	"strings"
	"sync"
)

// lineReader hands out stdin lines one at a time. At most one read is ever
// outstanding: a consumer that gives up (e.g. the browser delivered the
// CAPTCHA token first) leaves the pending read in place, and the next consumer
// receives that line instead of racing it.
type lineReader struct {
	mu      sync.Mutex
	r       *bufio.Reader
	pending chan string
}

func newLineReader(r io.Reader) *lineReader {
	return &lineReader{r: bufio.NewReader(r)}
}

// next returns a channel that yields the next line, or closes at EOF.
func (l *lineReader) next() <-chan string {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.pending != nil {
		return l.pending
	}
	ch := make(chan string, 1)
	l.pending = ch
	go func() {
		line, err := l.r.ReadString('\n')
		l.mu.Lock()
		l.pending = nil
		l.mu.Unlock()
		if line != "" || err == nil {
			ch <- strings.TrimRight(line, "\r\n")
		}
		close(ch)
	}()
	return ch
}

var stdinLines = newLineReader(os.Stdin)
