require 'nokogiri'

def name_for_rgba_components(red, green, blue, alpha)
    case format('#%02X%02X%02X%02X', red, green, blue, alpha)
    # Return named color matching RGBA components
    # e.g. "#F8CB00FF" => "Accent"
    end
end

def name_for_white_and_alpha_components(white, alpha)
    # Return named color matching white and alpha components
    # e.g. 0.9 => "Off-White"
end

# Process each Storyboard and XIB file
Dir['**/*.{storyboard,xib}'].each do |xib|
  doc = Nokogiri::XML(File.read(xib))

  names = []
  # Collect each custom color and assign it a name
  doc.xpath('//objects//color').each do |color|
    next if color['name']

    name = nil

    color_space = color['colorSpace']
    color_space = color['customColorSpace'] if color_space == 'custom'

    case color_space
    when 'sRGB', 'calibratedRGB'
      components = color.attributes
                        .values_at('red', 'green', 'blue', 'alpha')
                        .map(&:value)
                        .map(&:to_f)
                        .map { |c| c * 255 }
      name = name_for_rgba_components(*components)
    when 'genericGamma22GrayColorSpace', 'calibratedWhite'
      components = color.attributes
                        .values_at('white', 'alpha')
                        .map(&:value)
                        .map(&:to_f)
      name = name_for_white_and_alpha_components(*components)
    end

    next unless name

    named_color = doc.create_element('color',
                                     key: color['key'],
                                     name: name)
    color.replace(named_color)
    names << name
  end

  # Proceed to the next file if no named colors were found
  next if names.empty?

  # Add the named color capability as a document dependency
  dependencies = doc.at('/document/dependencies') ||
                 doc.root.add_child(doc.create_element('dependencies'))
  unless dependencies.at("capability[@name='Named colors']")
    dependencies << doc.create_element('capability',
                                       name: 'Named colors',
                                       minToolsVersion: '9.0')
  end

  # Add each named color to the document resources
  resources = doc.at('/document/resources') ||
              doc.root.add_child(doc.create_element('resources'))
  names.uniq.sort.each do |name|
    next if resources.at("namedColor[@name='#{name}']")
    resources << doc.create_element('namedColor', name: name)
  end

  # Save the changes
  File.write(xib, doc.to_xml(indent: 4, encoding: 'UTF-8'))
end
