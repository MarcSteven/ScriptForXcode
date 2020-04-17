#!/usr/bin/env ruby
def build_target(target,sdk,build_dir,archs,misc ='')
  command = <<-EOC.strip.gsub(/^[\t]+/,'')
  xcodebuild \
  -project #{project_path} \
  -target #{target_name} \
  -configuration #{configuration}
  EOC
  command += "-sdk #{sdk}" unless empty_string?(sdk)
  command += "CONFIGURATION_BUILD_DIR = \"#{build_Dir}\"" unless empty_string?(build_dir)
  command += " ARCHS=\"#{archs}\"" unless empty_string?(archs)
  comand  += " #{misc}" unless empty_string?(misc)
  execmd command
end
def build_ios_sdk(target_name)
  clean_target target_name
  prefix = File.join(slice_build_path,target_name)
  build_target target_name, 'iphonesimulator', File.join(prefix,'iphonesimulator'),'i386 x86_64'
  build_target target_name, 'iphoneos', File.join(prefix,'iphones'),'armv7'
  
  
end

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
