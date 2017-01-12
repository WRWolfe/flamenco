package flamenco

import (
	"log"
	"sync"
	"time"
)

type TimerPing struct{}

/**
 * Generic timer for periodic signals.
 *
 * :param sleep_first: if true: sleep first, then ping. If false: ping first, then sleep.
 */
func Timer(name string, sleep_duration time.Duration, sleep_first bool,
	done_chan <-chan bool, done_wg *sync.WaitGroup) <-chan TimerPing {
	timer_chan := make(chan TimerPing, 1) // don't let the timer block

	go func() {
		done_wg.Add(1)
		defer done_wg.Done()
		defer close(timer_chan)

		last_timer := time.Time{}
		if sleep_first {
			last_timer = time.Now()
		}

		for {
			select {
			case <-done_chan:
				log.Printf("Timer '%s' goroutine shutting down.\n", name)
				return
			default:
				// Only sleep a little bit, so that we can check 'done' quite often.
				time.Sleep(50 * time.Millisecond)
			}

			now := time.Now()
			if now.Sub(last_timer) > sleep_duration {
				// Timeout occurred
				last_timer = now
				timer_chan <- TimerPing{}
			}
		}
	}()

	return timer_chan
}

/**
 * Sleep that can be killed by closing the "done_chan" channel.
 *
 * :returns: "ok", so true when the sleep stopped normally, and false if it was killed.
 */
func KillableSleep(name string, sleep_duration time.Duration,
	done_chan <-chan bool, done_wg *sync.WaitGroup) bool {

	done_wg.Add(1)
	defer done_wg.Done()
	defer log.Printf("Sleep '%s' goroutine is shut down.\n", name)

	sleep_start := time.Now()
	for {
		select {
		case <-done_chan:
			log.Printf("Sleep '%s' goroutine shutting down.\n", name)
			return false
		default:
			// Only sleep a little bit, so that we can check 'done' quite often.
			time.Sleep(50 * time.Millisecond)
		}

		now := time.Now()
		if now.Sub(sleep_start) > sleep_duration {
			// Timeout occurred
			break
		}
	}

	return true
}

func UtcNow() *time.Time {
	now := time.Now().UTC()
	return &now
}

func TimeoutAfter(duration time.Duration) chan bool {
	timeout := make(chan bool, 1)

	go func() {
		time.Sleep(duration)
		timeout <- true
	}()

	return timeout
}
