#!/usr/bin/env ruby


def merge_framework(prefix,target_name)
  product_name = product_name(target_name)
  
  frameworks = Dir.glob(File.join(prefix,'*',"#{product_name}.framework"))
  first_framework = frameworks.first
  
  return if first_framework.nil?
  
  output = File.join(build_path,"#{target_name}.framework")
  execmd "cp-RLp #{first_framework} #{output}"
  
  return if frameworks.count == 1
  executables = frameworks.map {|framework| File.join(framework,product_name)}
  lipo File.join(output,product_name),*executables
  
  
  
  
  
  
  
  end
