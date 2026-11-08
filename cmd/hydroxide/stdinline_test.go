package main

import (
	"strings"
	"testing"
	"time"
)

func recv(t *testing.T, ch <-chan string) (string, bool) {
	t.Helper()
	select {
	case v, ok := <-ch:
		return v, ok
	case <-time.After(2 * time.Second):
		t.Fatal("timed out waiting for a line")
		return "", false
	}
}

// A consumer that abandons its read must not swallow the next line.
func TestAbandonedReadDoesNotLoseLine(t *testing.T) {
	l := newLineReader(strings.NewReader("123456\nsecond\n"))

	first := l.next() // consumer A starts a read, then gives up
	second := l.next()
	if first != second {
		t.Fatal("expected the pending read to be shared, not duplicated")
	}
	if v, _ := recv(t, second); v != "123456" {
		t.Fatalf("got %q, want 123456", v)
	}
	if v, _ := recv(t, l.next()); v != "second" {
		t.Fatalf("got %q, want second", v)
	}
}

func TestEOFClosesChannel(t *testing.T) {
	l := newLineReader(strings.NewReader(""))
	if _, ok := recv(t, l.next()); ok {
		t.Fatal("expected closed channel at EOF")
	}
}
