#!/usr/bin/ruby

def sortProperties(lines)
	props = Hash.new
	lines.each {|line|
		props[line.gsub(/@.+?(\w+?);[^;]*?$/, "\\1")] = line
	}
	
	sortedKeys = props.keys.sort
	
	output = Array.new
	sortedKeys.each { |key|
		output << props[key]
	}
	return output
end

def sortMethods(lines)
	methods = Hash.new
	lines.each {|line|
		methods[line.gsub(/^[-+ ]+\([\w \*]+\) *(.+)/, "\\1")] = line
	}
	
	sortedKeys = methods.keys.sort
	
	output = Array.new
	sortedKeys.each { |key|
		output << methods[key]	
	}
	
	return output
end

lines = Array.new
ARGF.each {|line|
	lines << line	
}

classMethods = Array.new
instanceMethods = Array.new
properties = Array.new

lines.each {|line|
	if line.start_with?("+") 
		classMethods << line
	elsif  line.start_with?("-") 
		instanceMethods << line
	elsif line.start_with?("@property") 
		properties << line	
	end
}

puts "\n\n// Class Methods\n"
puts sortMethods(classMethods)
puts "\n\n// Properties\n"
puts sortProperties(properties)
puts "\n\n// Instance Methods\n"
puts sortMethods(instanceMethods)
