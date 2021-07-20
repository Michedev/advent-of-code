require 'set'
require_relative 'parser'

class GameRunner

    def initialize(data, turn_end=2020)
        @turn_end = turn_end
        @number_last_two_spoken = {}
        data.each_with_index do |el, idx|
            @number_last_two_spoken[el] = [idx+1, -1]
        end
        @last_number = data[-1]
        @turn = data.length + 1
    end

    def has_been_spoken(number)
        @number_last_two_spoken.keys.include?(number) and @number_last_two_spoken[number][1] != -1
    end

    def last_two_call_diff(number)
        t1, t2 = @number_last_two_spoken[number]
        t1 - t2
    end

    def run
        while @turn <= @turn_end
            if not has_been_spoken @last_number
                next_number = 0
            else
                next_number = last_two_call_diff @last_number
            end
            if not @number_last_two_spoken.keys.include? next_number
                @number_last_two_spoken[next_number] = [@turn, -1]
            else
                last_turn_number = @number_last_two_spoken[next_number][0]
                @number_last_two_spoken[next_number] = [@turn, last_turn_number]
            end
            @last_number = next_number
            @turn += 1
        end
        @last_number
    end

end


data = read_file
g = GameRunner.new(data)
puts g.run
