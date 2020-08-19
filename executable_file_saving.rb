#!/usr/bin/ruby

=begin
#### DIRECTIONS ####
Run `/usr/bin/ruby savings.rb <path to executable>`, and it will report the estimated savings for that executable.
*However*, the executable cannot have been downloaded from the app store (or else it will already be the encrypted version, and we can't unencrypt it to calculate the savings)
Also, it should be a binary for a specific architecture, and not a fat binary. I'd assume arm64 would be way to go.
How to get an arm64 binary that is not encrypted?
Run Product -> Archive in Xcode, then export the app Ad Hoc, and for the device to thin for, select a device with arm64 (an iPhone 5s or above) 
Unzip the .ipa file that was exported, and Payload/<app name>.app/<app name> should be the executable that you want
=end


def fill_with_random(tmp_dir, path)
  lines = `xcrun size -x -l -m #{path}`.split("\n")
  lines = lines.drop_while do |line|
    !line.start_with?("Segment __TEXT: ")
  end.drop(1)
  first_line = lines.first
  lines = lines.take_while do |line|
    !line.start_with?("Segment __DATA: ")
  end
  total_line = lines.last
  start = first_line.match(/^\s*Section \S+ \S+ \(addr \S+ offset (\d+)/)[1].to_i
  size = total_line.match(/^\s*total (\S+)/)[1].to_i(16)

  bs = 100
  str = "dd if=/dev/urandom of=#{path} bs=#{bs} count=#{size/bs} seek=#{start/bs} conv=notrunc > /dev/null 2>&1"
  `#{str}`
end

def magic_header(path)
  return nil unless File.size(path) >= 4
  File.open(path).read(4).each_char.map { |c| c.ord.to_s(16) }.join("").to_i(16)
end

raise "Usage: /usr/bin/ruby savings.rb <path to the executable within the Payload folder>" unless ARGV.size == 1
path = File.absolute_path(ARGV.first)

arm64_headers = [0xFEEDFACF, 0xCFFAEDFE]

raise "File must be an arm64 executable" unless arm64_headers.include?(magic_header(path))

dir = "/tmp/size_dir"
`rm -r #{dir}`
`mkdir #{dir}`
Dir.chdir(dir)
`cp "#{path}" unenc`
`zip -r unenc.zip unenc`
unenc_size = File.size("unenc.zip")
enc_path = "enc"
`cp "#{path}" #{enc_path}`
fill_with_random(dir, enc_path)
`zip -r enc.zip #{enc_path}`
enc_size = File.size("enc.zip")
puts "#{enc_size - unenc_size} bytes would be saved"
