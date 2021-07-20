def read_file
    File.read("input_example.txt").split(",").map { |el| el.to_i}
end
